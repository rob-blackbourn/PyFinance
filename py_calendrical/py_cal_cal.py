# use true division
from __future__ import division

# Precision in bits, for places where CL postfixes numbers with L0, meaning
# at least 50 bits of precision
import math
from mpmath import *
from enum import IntEnum, Enum
mp.prec = 50

def even(i):
    return mod(i, 2) == 0

def odd(i):
    return not even(i)

# I (re)define floor: in CL it always returns an integer.
# I make it explicit the fact it returns an integer by
# naming it ifloor
def ifloor(n):
    """Return the whole part of m/n."""
    return int(math.floor(n))

# see lines 249-252 in calendrica-3.0.cl
# m // n
# The following
#      from operator import floordiv as quotient
# is not ok, the corresponding CL code
# uses CL 'floor' which always returns an integer
# (the floating point equivalent is 'ffloor'), while
# 'quotient' from operator module (or corresponding //)
# can return a float if at least one of the operands
# is a float...so I redefine it (and 'floor' and 'round' as well: in CL
# they always return an integer.)
def quotient(m, n):
    """Return the whole part of m/n towards negative infinity."""
    return ifloor(m / n)

# I (re)define round: in CL it always returns an integer.
# I make it explicit the fact it returns an integer by
# naming it iround
def iround(n):
    """Return the whole part of m/n."""
    return int(round(n))


# m % n   (this works as described in book for negative integres)
# It is interesting to note that
#    mod(1.5, 1)
# returns the decimal part of 1.5, so 0.5; given a moment 'm'
#    mod(m, 1)
# returns the time of the day
from operator import mod

def amod(x, y):
    """Return the same as a % b with b instead of 0."""
    return y + (mod(x, -y))

def signum(a):
    if a > 0:
        return 1
    elif a == 0:
        return 0
    else:
        return -1

# see lines 2380-2390 in calendrica-3.0.cl
# The following
#      from math import ceil as iceiling
# is not ok, the corresponding CL code
# uses CL iceiling which always returns and integer, while
# ceil from math module always returns a float...so I redefine it
def iceiling(n):
    """Return the integer rounded towards +infinitum of n."""
    return int(math.ceil(n))

def next_int(i, p):
    """Return first integer greater or equal to initial index, i,
    such that condition, p, holds."""
    return i if p(i) else next_int(i + 1, p)

def final_int(i, p):
    """Return last integer greater or equal to initial index, i,
    such that condition, p, holds."""
    return i - 1 if not p(i) else final_int(i + 1, p)

def summa(f, k, p):
    """Return the sum of f(i) from i=k, k+1, ... till p(i) holds true or 0.
    This is a tail recursive implementation."""
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
    p determines when to go left."""
    x = (lo + hi) / 2
    if p(lo, hi):
        return x
    elif e(x):
        return binary_search(lo, x, p, e)
    else:
        return binary_search(x, hi, p, e)

def invert_angular(f, y, a, b, prec=10 ** -5):
    """Find inverse of angular function 'f' at 'y' within interval [a,b].
    Default precision is 0.00001"""
    return binary_search(a, b,
                         (lambda l, h: ((h - l) <= prec)),
                         (lambda x: mod((f(x) - y), 360) < 180))
#def invert_angular(f, y, a, b):
#      from scipy.optimize import brentq
#    return(brentq((lambda x: mod(f(x) - y), 360)), a, b, xtol=error)

def sigma(l, b):
    """Return the sum of body 'b' for indices i1..in
    running simultaneously thru lists l1..ln.
    List 'l' is of the form [[i1 l1]..[in ln]]"""
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

def poly(x, a):
    """Calculate polynomial with coefficients 'a' at point x.
    The polynomial is a[0] + a[1] * x + a[2] * x^2 + ...a[n-1]x^(n-1)
    the result is
    a[0] + x(a[1] + x(a[2] +...+ x(a[n-1])...)"""
    # This implementation is also known as Horner's Rule.
    n = len(a) - 1
    p = a[n]
    for i in range(1, n+1):
        p = p * x + a[n-i]
    return p

def secs(x):
    """Return the seconds in angle x."""
    return x / 3600

def angle(d, m, s):
    """Return an angle data structure
    from d degrees, m arcminutes and s arcseconds.
    This assumes that negative angles specifies negative d, m and s."""
    return d + ((m + (s / 60)) / 60)

def normalized_degrees(theta):
    """Return a normalize angle theta to range [0,360) degrees."""
    return mod(theta, 360)

def normalized_degrees_from_radians(theta):
    """Return normalized degrees from radians, theta.
    Function 'degrees' comes from mpmath."""
    return normalized_degrees(degrees(theta))

from mpmath import radians as radians_from_degrees

def sin_degrees(theta):
    """Return sine of theta (given in degrees)."""
    return sin(radians_from_degrees(theta))

def cos_degrees(theta):
    """Return cosine of theta (given in degrees)."""
    return cos(radians_from_degrees(theta))

def tan_degrees(theta):
    """Return tangent of theta (given in degrees)."""
    return tan(radians_from_degrees(theta))

#-----------------------------------------------------------
# NOTE: arc[tan|sin|cos] casted with degrees given CL code
#       returns angles [0, 360), see email from Dershowitz
#       after my request for clarification
#-----------------------------------------------------------

# see lines 2728-2739 in calendrica-3.0.cl
# def arctan_degrees(y, x):
#     """ Arctangent of y/x in degrees."""
#     from math import atan2
#     return normalized_degrees_from_radians(atan2(x, y))

def arctan_degrees(y, x):
    """ Arctangent of y/x in degrees."""
    if (x == 0) and (y != 0):
        return mod(signum(y) * mpf(90), 360)
    else:
        alpha = normalized_degrees_from_radians(atan(y / x))
        if x >= 0:
            return alpha
        else:
            return mod(alpha + mpf(180), 360)

def arcsin_degrees(x):
    """Return arcsine of x in degrees."""
    return normalized_degrees_from_radians(asin(x))

def arccos_degrees(x):
    """Return arccosine of x in degrees."""
    return normalized_degrees_from_radians(acos(x))

# Epoch definition. I took it out explicitly from rd().
def epoch():
    """Epoch definition. For Rata Diem, R.D., it is 0 (but any other reference
    would do.)"""
    return 0

def rd(tee):
    """Return rata diem (number of days since epoch) of moment in time, tee."""
    return tee - epoch()

def is_in_range(tee, pair):
    """Return True if moment 'tee' falls within range 'range',
    False otherwise."""
    return pair[0] <= tee <= pair[1]

def list_range(ell, pair):
    """Return those moments in list ell that occur in range 'pair'."""
    return filter(lambda x: is_in_range(x, pair), ell)

class DayOfWeek(IntEnum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

    @classmethod
    def from_fixed(cls, date):
        """Return day of the week from a fixed date 'date'."""
        return DayOfWeek(mod(date - rd(0) - DayOfWeek.Sunday, 7))

    def on_or_before(self, fixed_date):
        """Return the fixed date of the k-day on or before fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return fixed_date - DayOfWeek.from_fixed(fixed_date - self.value)
    
    def on_or_after(self, fixed_date):
        """Return the fixed date of the k-day on or after fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 6)
    
    def nearest(self, fixed_date):
        """Return the fixed date of the k-day nearest fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 3)
    
    def after(self, fixed_date):
        """Return the fixed date of the k-day after fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 7)
    
    def before(self, fixed_date):
        """Return the fixed date of the k-day before fixed date 'date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date - 1)

def standard_month(date):
    """Return the month of date 'date'."""
    return date[1]

def standard_day(date):
    """Return the day of date 'date'."""
    return date[2]

def standard_year(date):
    """Return the year of date 'date'."""
    return date[0]

class Clock(object):
    
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def to_time(self):
        """Return time of day from clock time 'hms'."""
        return(1/24 * (self.hour + ((self.minute + (self.second / 60)) / 60)))

    @classmethod
    def from_moment(cls, tee):
        """Return clock time hour:minute:second from moment 'tee'."""
        time = cls.time_from_moment(tee)
        hour = ifloor(time * 24)
        minute = ifloor(mod(time * 24 * 60, 60))
        second = mod(time * 24 * 60 * 60, 60)
        return Clock(hour, minute, second)

    @classmethod
    def fixed_from_moment(cls, tee):
        """Return fixed date from moment 'tee'."""
        return ifloor(tee)
    
    @classmethod
    def time_from_moment(cls, tee):
        """Return time from moment 'tee'."""
        return mod(tee, 1)

    @classmethod
    def days_from_hours(cls, x):
        """Return the number of days given x hours."""
        return x / 24
    
    @classmethod
    def days_from_seconds(cls, x):
        """Return the number of days given x seconds."""
        return x / 24 / 60 / 60

class DegreeMinutesSeconds(object):
    
    def __init__(self, degrees, minutes, seconds):
        self.degress = degrees
        self.minutes = minutes
        self.seconds = seconds

    @classmethod        
    def from_angle(cls, alpha):
        """Return an angle in degrees:minutes:seconds from angle,
        'alpha' in degrees."""
        d = ifloor(alpha)
        m = ifloor(60 * mod(alpha, 1))
        s = mod(alpha * 60 * 60, 60)
        return DegreeMinutesSeconds(d, m, s)

class JD(object):
    
    EPOCH = rd(mpf(-1721424.5))

    def __init__(self, date_from_epoch):
        self.date_from_epoch = date_from_epoch
    
    def to_moment(self):
        return self.date_from_epoch + self.EPOCH

    @classmethod
    def from_moment(cls, tee):
        return JD(tee - cls.EPOCH)
    
    def to_fixed(self):
        return ifloor(self.to_moment())

    @classmethod
    def from_fixed(cls, fixed_date):
        return cls.from_moment(fixed_date)

class MJD(object):
    
    EPOCH = rd(678576)

    def __init__(self, date_from_epoch):
        self.date_from_epoch = date_from_epoch

    def to_fixed(self):
        return self.date_from_epoch + self.EPOCH

    @classmethod
    def from_fixed(cls, fixed_date):
        return MJD(fixed_date - cls.EPOCH)


class JulianMonth(IntEnum):
    January = 1
    February = 2
    March = 3
    April = 4
    May = 5
    June = 6
    July = 7
    August = 8
    September = 9
    October = 10
    November = 11
    December = 12


class GregorianDate(object):    

    EPOCH = rd(1)

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_fixed(self):
        """Return the serial date equivalent."""
        return ((self.EPOCH - 1) + 
                (365 * (self.year -1)) + 
                quotient(self.year - 1, 4) - 
                quotient(self.year - 1, 100) + 
                quotient(self.year - 1, 400) + 
                quotient((367 * self.month) - 362, 12) + 
                (0 if self.month <= 2
                 else (-1 if self.is_leap_year(self.year) else -2)) +
                self.day)

    @classmethod
    def is_leap_year(cls, year):
        """Return True if 'year' is leap."""
        return (mod(year, 4) == 0) and (mod(year, 400) not in [100, 200, 300])
    
    @classmethod
    def to_year(cls, fixed_date):
        """Return the year corresponding to the fixed date 'fixed_date'."""
        d0   = fixed_date - cls.EPOCH
        n400 = quotient(d0, 146097)
        d1   = mod(d0, 146097)
        n100 = quotient(d1, 36524)
        d2   = mod(d1, 36524)
        n4   = quotient(d2, 1461)
        d3   = mod(d2, 1461)
        n1   = quotient(d3, 365)
        year = (400 * n400) + (100 * n100) + (4 * n4) + n1
        return year if (n100 == 4) or (n1 == 4) else (year + 1)

    @classmethod
    def new_year(cls, year):
        """Return the fixed date of January 1 in the year 'year'."""
        return GregorianDate(year, JulianMonth.January, 1).to_fixed()

    @classmethod
    def year_end(cls, year):
        """Return the fixed date of December 31 in the year 'year'."""
        return GregorianDate(year, JulianMonth.December, 31).to_fixed()

    @classmethod    
    def year_range(cls, year):
        """Return the range of fixed dates in the year 'g_year'."""
        return [cls.new_year(year), cls.year_end(year)]

    @classmethod    
    def from_fixed(cls, fixed_date):
        """Return the fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        year = cls.to_year(fixed_date)
        prior_days = fixed_date - cls.new_year(year)
        correction = (0
                      if (fixed_date < GregorianDate(year, JulianMonth.March, 1).to_fixed())
                      else (1 if cls.is_leap_year(year) else 2))
        month = quotient((12 * (prior_days + correction)) + 373, 367)
        day = 1 + (fixed_date - GregorianDate(year, month, 1).to_fixed())
        return GregorianDate(year, month, day)

    @classmethod    
    def date_difference(cls, date1, date2):
        """Return the number of days from date 'date1'
        till date 'date2'."""
        return date2.to_fixed() - date1.to_fixed()
    
    def day_number(self):
        """Return the day number in the year."""
        return self.date_difference(GregorianDate(self.year - 1, JulianMonth.December, 31), self)
    
    def days_remaining(self):
        """Return the days remaining in the year."""
        return self.date_difference(self, GregorianDate(self.year, JulianMonth.December, 31))
    
    def to_fixed_alt(self):
        """Return the fixed date equivalent.
        Alternative calculation."""
        m     = amod(self.month - 2, 12)
        y     = self.year + quotient(self.month + 9, 12)
        return ((self.EPOCH - 1)  +
                -306                   +
                365 * (y - 1)          +
                quotient(y - 1, 4)     +
                -quotient(y - 1, 100)  +
                quotient(y - 1, 400)   +
                quotient(3 * m - 1, 5) +
                30 * (m - 1)           +
                self.day)

    @classmethod    
    def to_gregorian_alt(cls, fixed_date):
        """Return the date corresponding to fixed date 'fixed_date'.
        Alternative calculation."""
        y = cls.to_year(cls.EPOCH - 1 + fixed_date + 306)
        prior_days = fixed_date - GregorianDate(y - 1, JulianMonth.March, 1).to_fixed()
        month = amod(quotient(5 * prior_days + 2, 153) + 3, 12)
        year  = y - quotient(month + 9, 12)
        day   = fixed_date - GregorianDate(year, month, 1).to_fixed() + 1
        return GregorianDate(year, month, day)
    
    @classmethod    
    def to_year_alt(cls, fixed_date):
        """Return the year corresponding to the fixed date 'fixed_date'.
        Alternative calculation."""
        approx = quotient(fixed_date - cls.EPOCH +2, 146097/400)
        start  = (cls.EPOCH        +
                  (365 * approx)         +
                  quotient(approx, 4)    +
                  -quotient(approx, 100) +
                  quotient(approx, 400))
        return approx if (fixed_date < start) else (approx + 1)

    def nth_day_of_week(self, n, day_of_week):
        """Return the fixed date of n-th day of week.
        If n>0, return the n-th day of week on or after this date.
        If n<0, return the n-th day of week on or before this date.
        If n=0, return raise an error.
        A k-day of 0 means Sunday, 1 means Monday, and so on."""
        if n > 0:
            return 7*n + day_of_week.before(self.to_fixed())
        elif n < 0:
            return 7*n + day_of_week.after(self.to_fixed())
        else:
            raise ValueError("No valid answer where 'n' == 0.")

    def first_day_of_week(self, day_of_week):
        """Return the fixed date of first day of week on or after this date."""
        return self.nth_day_of_week(1, day_of_week)
    
    def last_day_of_week(self, day_of_week):
        """Return the fixed date of last day of week on or before this date."""
        return self.nth_day_of_week(-1, day_of_week)

#     @classmethod
#     def orthodox_easter(cls, year):
#         """Return fixed date of Orthodox Easter in Gregorian year g_year."""
#         shifted_epact = mod(14 + 11 * mod(year, 19), 30)
#         j_year        = year if year > 0 else year - 1
#         paschal_moon  = JulianDate(j_year, JulianMonth.April, 19).to_fixed() - shifted_epact
#         return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)
    
    @classmethod
    def alt_orthodox_easter(cls, year):
        """Return fixed date of Orthodox Easter in Gregorian year g_year.
        Alternative calculation."""
        paschal_moon = (354 * year +
                        30 * quotient((7 * year) + 8, 19) +
                        quotient(year, 4)  -
                        quotient(year, 19) -
                        273 +
                        cls.EPOCH)
        return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)
    
    @classmethod
    def easter(cls, year):
        """Return fixed date of Easter in Gregorian year g_year."""
        century = quotient(year, 100) + 1
        shifted_epact = mod(14 +
                            11 * mod(year, 19) -
                            quotient(3 * century, 4) +
                            quotient(5 + (8 * century), 25), 30)
        adjusted_epact = ((shifted_epact + 1)
                          if ((shifted_epact == 0) or ((shifted_epact == 1) and
                                                      (10 < mod(year, 19))))
                          else  shifted_epact)
        paschal_moon = (GregorianDate(year, JulianMonth.April, 19).to_fixed() - adjusted_epact)
        return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)

    @classmethod    
    def pentecost(cls, year):
        """Return fixed date of Pentecost in Gregorian year g_year."""
        return cls.easter(year) + 49

#     @classmethod
#     def eastern_orthodox_christmas(cls, g_year):
#         """Return the list of zero or one fixed dates of Eastern Orthodox Christmas
#         in Gregorian year 'g_year'."""
#         return JulianDate.julian_in_gregorian(JulianMonth.December, 25, g_year)

    @classmethod
    def labor_day(cls, g_year):
        """Return the fixed date of United States Labor Day in Gregorian
        year 'g_year' (the first Monday in September)."""
        return GregorianDate(g_year, JulianMonth.September, 1).first_day_of_week(DayOfWeek.Monday)

    @classmethod
    def memorial_day(cls, g_year):
        """Return the fixed date of United States' Memorial Day in Gregorian
        year 'g_year' (the last Monday in May)."""
        return GregorianDate(g_year, JulianMonth.May, 31).last_day_of_week(DayOfWeek.Monday)
    
    @classmethod
    def election_day(cls, g_year):
        """Return the fixed date of United States' Election Day in Gregorian
        year 'g_year' (the Tuesday after the first Monday in November)."""
        return GregorianDate(g_year, JulianMonth.November, 2).first_day_of_week(DayOfWeek.Tuesday)

    @classmethod
    def daylight_saving_start(cls, g_year):
        """Return the fixed date of the start of United States daylight
        saving time in Gregorian year 'g_year' (the second Sunday in March)."""
        return GregorianDate(g_year, JulianMonth.March, 1).nth_day_of_week(2, DayOfWeek.Sunday)

    @classmethod
    def daylight_saving_end(cls, g_year):
        """Return the fixed date of the end of United States daylight saving
        time in Gregorian year 'g_year' (the first Sunday in November)."""
        return GregorianDate(g_year, JulianMonth.November, 1).first_day_of_week(DayOfWeek.Sunday)
    
    @classmethod
    def christmas(cls, g_year):
        """Return the fixed date of Christmas in Gregorian year 'g_year'."""
        return GregorianDate(g_year, JulianMonth.December, 25).to_fixed()

    @classmethod    
    def advent(cls, g_year):
        """Return the fixed date of Advent in Gregorian year 'g_year'
        (the Sunday closest to November 30)."""
        return DayOfWeek(DayOfWeek.Sunday).nearest(GregorianDate(g_year, JulianMonth.November, 30).to_fixed())
    @classmethod
    def epiphany(cls, g_year):
        """Return the fixed date of Epiphany in U.S. in Gregorian year 'g_year'
        (the first Sunday after January 1)."""
        return GregorianDate(g_year, JulianMonth.January, 2).first_day_of_week(DayOfWeek.Sunday)

    @classmethod
    def epiphany_it(cls, g_year):
        """Return fixed date of Epiphany in Italy in Gregorian year 'g_year'."""
        return GregorianDate(g_year, JulianMonth.January, 6)

    @classmethod
    def unlucky_fridays_in_range(cls, range):
        """Return the list of Fridays within range 'range' of fixed dates that
        are day 13 of the relevant Gregorian months."""
        a    = range[0]
        b    = range[1]
        fri  = DayOfWeek(DayOfWeek.Friday).on_or_after(a)
        date = GregorianDate.from_fixed(fri)
        ell  = [fri] if (standard_day(date) == 13) else []
        if is_in_range(fri, range):
            ell[:0] = cls.unlucky_fridays_in_range([fri + 1, b])
            return ell
        else:
            return []








    








######################
# Time and Astronomy #
######################



