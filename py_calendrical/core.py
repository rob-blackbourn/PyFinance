from __future__ import division
from mpmath import mp
mp.prec = 50

def quotient(m, n):
    """Return the whole part of m/n towards negative infinity.
        
    See lines 249-252 in calendrica-3.0.cl
    m // n
    The following from operator import floordiv as quotient
    is not ok, the corresponding CL code
    uses CL 'floor' which always returns an integer
    (the floating point equivalent is 'ffloor'), while
    'quotient' from operator module (or corresponding //)
    can return a float if at least one of the operands
    is a float...so I redefine it (and 'floor' and 'round' as well: in CL
    they always return an integer.)
    """
    return ifloor(m / n)

def ifloor(n):
    """Return the whole part of m/n.
    
    I (re)define floor: in CL it always returns an integer.
    I make it explicit the fact it returns an integer by
    naming it ifloor.
    """
    from math import floor
    return int(floor(n))

def iround(n):
    """Return the whole part of m/n.
    
    I (re)define round: in CL it always returns an integer.
    I make it explicit the fact it returns an integer by
    naming it iround.
    """
    from __builtin__ import round
    return int(round(n))

# see lines 2380-2390 in calendrica-3.0.cl
# The following
#      from math import ceil as ceiling
# is not ok, the corresponding CL code
# uses CL ceiling which always returns and integer, while
# ceil from math module always returns a float...so I redefine it
def ceiling(n):
    """Return the integer rounded towards +infinitum of n."""
    from math import ceil
    return int(ceil(n))

# m % n   (this works as described in book for negative integres)
# It is interesting to note that
#    mod(1.5, 1)
# returns the decimal part of 1.5, so 0.5; given a moment 'm'
#    mod(m, 1)
# returns the time of the day
from operator import mod


# see lines 402-405 in calendrica-3.0.cl
def fixed_from_moment(tee):
    """Return fixed date from moment 'tee'."""
    return ifloor(tee)

def amod(x, y):
    """Return the same as a % b with b instead of 0.
    
    see lines 254-257 in calendrica-3.0.cl
    """
    return y + (mod(x, -y))

def next(i, p):
    """Return first integer greater or equal to initial index, i,
    such that condition, p, holds.
    
    # see lines 259-264 in calendrica-3.0.cl
    """
    return i if p(i) else next(i + 1, p)

def final(i, p):
    """Return last integer greater or equal to initial index, i,
    such that condition, p, holds.
    
    see lines 266-271 in calendrica-3.0.cl
    """
    return i - 1 if not p(i) else final(i + 1, p)

def summa(f, k, p):
    """Return the sum of f(i) from i=k, k+1, ... till p(i) holds true or 0.
    This is a tail recursive implementation.
    
    see lines 273-281 in calendrica-3.0.cl
    """
    return 0 if not p(k) else f(k) + summa(f, k + 1, p)

def altsumma(f, k, p):
    """Return the sum of f(i) from i=k, k+1, ... till p(i) holds true or 0.
    This is an implementation of the Summation formula from Kahan,
    see Theorem 8 in Goldberg, David 'What Every Computer Scientist
    Should Know About Floating-Point Arithmetic', ACM Computer Survey,
    Vol. 23, No. 1, March 1991."""
    if not p(k):
        return 0
    else:
        S = f(k)
        C = 0
        j = k + 1
        while p(j):
            Y = f(j) - C
            T = S + Y
            C = (T - S) - Y
            S = T
            j += 1
    return S

def binary_search(lo, hi, p, e):
    """Bisection search for x in [lo, hi] such that condition 'e' holds.
    p determines when to go left.
    
    see lines 283-293 in calendrica-3.0.cl
    """
    x = (lo + hi) / 2
    if p(lo, hi):
        return x
    elif e(x):
        return binary_search(lo, x, p, e)
    else:
        return binary_search(x, hi, p, e)


def invert_angular(f, y, a, b, prec=10 ** -5):
    """Find inverse of angular function 'f' at 'y' within interval [a,b].
    Default precision is 0.00001
    
    # see lines 295-302 in calendrica-3.0.cl
    """
    return binary_search(a, b,
                         (lambda l, h: ((h - l) <= prec)),
                         (lambda x: mod((f(x) - y), 360) < 180))

#def invert_angular(f, y, a, b):
#      from scipy.optimize import brentq
#    return(brentq((lambda x: mod(f(x) - y), 360)), a, b, xtol=error)


def sigma(l, b):
    """Return the sum of body 'b' for indices i1..in
    running simultaneously thru lists l1..ln.
    List 'l' is of the form [[i1 l1]..[in ln]]
    
    see lines 304-313 in calendrica-3.0.cl
    """
    # 'l' is a list of 'n' lists of the same lenght 'L' [l1, l2, l3, ...]
    # 'b' is a lambda with 'n' args
    # 'sigma' sums all 'L' applications of 'b' to the relevant tuple of args
    # >>> a = [ 1, 2, 3, 4]
    # >>> b = [ 5, 6, 7, 8]
    # >>> c = [ 9,10,11,12]
    # >>> l = [a,b,c]
    # >>> z = zip(*l)
    # >>> z
    # [(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
    # >>> b = lambda x, y, z: x * y * z
    # >>> b(*z[0]) # apply b to first elem of i
    # 45
    # >>> temp = []
    # >>> z = zip(*l)
    # >>> for e in z: temp.append(b(*e))
    # >>> temp
    # [45, 120, 231, 384]
    # >>> from operator import add
    # >>> reduce(add, temp)
    # 780
    return sum(b(*e) for e in zip(*l))


from copy import copy
def poly(x, a):
    """Calculate polynomial with coefficients 'a' at point x.
    The polynomial is a[0] + a[1] * x + a[2] * x^2 + ...a[n-1]x^(n-1)
    the result is
    a[0] + x(a[1] + x(a[2] +...+ x(a[n-1])...)"
    
    see lines 315-321 in calendrica-3.0.cl
    """
    # This implementation is also known as Horner's Rule.
    n = len(a) - 1
    p = a[n]
    for i in range(1, n+1):
        p = p * x + a[n-i]
    return p

def epoch():
    """Epoch definition. For Rata Diem, R.D., it is 0 (but any other reference
    would do.)
    
    see lines 323-329 in calendrica-3.0.cl
    Epoch definition. I took it out explicitly from rd().
    """
    return 0

def rd(tee):
    """Return rata diem (number of days since epoch) of moment in time, tee."""
    return tee - epoch()
