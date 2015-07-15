from __future__ import division
from operator import mod

def reduce_cond(function, condition, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        try:
            initializer = next(it)
        except StopIteration:
            raise TypeError('reduce() of empty sequence with no initial value')
    accum_value = initializer
    for x in it:
        accum_value = function(accum_value, x)
        if not condition(accum_value, x):
            break
    return accum_value

def even(i):
    return mod(i, 2) == 0

def odd(i):
    return not even(i)

def next_int(i, p):
    """Return first integer greater or equal to initial index, i,
    such that condition, p, holds."""
    return i if p(i) else next_int(i + 1, p)

def final_int(i, p):
    """Return last integer greater or equal to initial index, i,
    such that condition, p, holds."""
    return i - 1 if not p(i) else final_int(i + 1, p)

def is_in_range(tee, pair):
    """Return True if moment 'tee' falls within range 'range',
    False otherwise."""
    return pair[0] <= tee <= pair[1]

def list_range(ell, pair):
    """Return those moments in list ell that occur in range 'pair'."""
    return filter(lambda x: is_in_range(x, pair), ell)
