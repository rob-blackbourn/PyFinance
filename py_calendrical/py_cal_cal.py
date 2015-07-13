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

class EgyptianDate(object):

    EPOCH = JD(1448638).to_fixed()    

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        
    def to_fixed(self):
        return self.EPOCH + (365*(self.year - 1)) + (30*(self.month - 1)) + (self.day - 1)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Egyptian fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        days = fixed_date - cls.EPOCH
        year = 1 + quotient(days, 365)
        month = 1 + quotient(mod(days, 365), 30)
        day = days - (365*(year - 1)) - (30*(month - 1)) + 1
        return EgyptianDate(year, month, day)

class ArmenianDate(object):

    EPOCH = rd(201443)
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_fixed(self):
        """Return the fixed date."""
        return (self.EPOCH +
                EgyptianDate(self.year, self.month, self.day).to_fixed() -
                EgyptianDate.EPOCH)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Armenian fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        ymd = EgyptianDate.from_fixed(fixed_date + (EgyptianDate.EPOCH - cls.EPOCH))
        return ArmenianDate(ymd.year, ymd.month, ymd.day)

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

class JulianDate(object):
    
    EPOCH = GregorianDate(0, JulianMonth.December, 30).to_fixed()
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        
    @classmethod
    def bce(cls, n):
        """Return a negative value to indicate a BCE Julian year."""
        return -n
    
    @classmethod
    def ce(cls, n):
        """Return a positive value to indicate a CE Julian year."""
        return n

    @classmethod
    def is_leap_year(cls, year):
        """Return True if Julian year 'year' is a leap year in
        the Julian calendar."""
        return mod(year, 4) == (0 if year > 0 else 3)

    def to_fixed(self):
        """Return the fixed date equivalent to the Julian date 'j_date'."""
        y     = self.year + 1 if self.year < 0 else self.year
        return (self.EPOCH - 1 +
                (365 * (y - 1)) +
                quotient(y - 1, 4) +
                quotient(367*self.month - 362, 12) +
                (0 if self.month <= 2 else (-1 if self.is_leap_year(self.year) else -2)) +
                self.day)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Julian fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        approx     = quotient(((4 * (fixed_date - cls.EPOCH))) + 1464, 1461)
        year       = approx - 1 if approx <= 0 else approx
        prior_days = fixed_date - JulianDate(year, JulianMonth.January, 1).to_fixed()
        correction = (0 if fixed_date < JulianDate(year, JulianMonth.March, 1).to_fixed()
                      else (1 if cls.is_leap_year(year) else 2))
        month      = quotient(12*(prior_days + correction) + 373, 367)
        day        = 1 + (fixed_date - JulianDate(year, month, 1).to_fixed())
        return JulianDate(year, month, day)

    @classmethod
    def julian_year_from_auc_year(cls, year):
        """Return the Julian year equivalent to AUC year 'year'."""
        return ((year + cls.YEAR_ROME_FOUNDED - 1) 
                if (1 <= year <= (year - cls.YEAR_ROME_FOUNDED))
                else (year + cls.YEAR_ROME_FOUNDED))
    
    @classmethod
    def auc_year_from_julian_year(cls, year):
        """Return the AUC year equivalent to Julian year 'year'."""
        return ((year - cls.YEAR_ROME_FOUNDED - 1)
                if (cls.YEAR_ROME_FOUNDED <= year <= -1)
                else (year - cls.YEAR_ROME_FOUNDED))
    
    
    @classmethod
    def julian_in_gregorian(j_month, j_day, g_year):
        """Return the list of the fixed dates of Julian month 'j_month', day
        'j_day' that occur in Gregorian year 'g_year'."""
        jan1 = GregorianDate.new_year(g_year)
        y    = JulianDate.from_fixed(jan1).year
        y_prime = 1 if (y == -1) else (y + 1)
        date1 = JulianDate(y, j_month, j_day).to_fixed()
        date2 = JulianDate(y_prime, j_month, j_day).to_fixed()
        return list_range([date1, date2], GregorianDate.year_range(g_year))

    @classmethod
    def eastern_orthodox_christmas(cls, g_year):
        """Return the list of zero or one fixed dates of Eastern Orthodox Christmas
        in Gregorian year 'g_year'."""
        return cls.julian_in_gregorian(JulianMonth.December, 25, g_year)

class Event(Enum):
    Kalends = 1
    Nones = 2
    Ides = 3
    
class RomanDate(object):
    
    YEAR_ROME_FOUNDED = JulianDate.bce(753)

    def __init__(self, year, month, event, count, leap):
        self.year = year
        self.month = month
        self.event = event
        self.count = count
        self.leap = leap

    @classmethod
    def ides_of_month(cls, month):
        """Return the date of the Ides in Roman month 'month'."""
        return 15 if month in [JulianMonth.March, JulianMonth.May, JulianMonth.July, JulianMonth.October] else 13

    @classmethod
    def nones_of_month(cls, month):
        """Return the date of Nones in Roman month 'month'."""
        return cls.ides_of_month(month) - 8

    def to_fixed(self):
        """Return the fixed date."""
        return ({Event.Kalends: JulianDate(self.year, self.month, 1).to_fixed(),
                 Event.Nones:   JulianDate(self.year, self.month, self.nones_of_month(self.month)).to_fixed(),
                 Event.Ides:    JulianDate(self.year, self.month, self.ides_of_month(self.month)).to_fixed()
                 }[self.event] -
                self.count +
                (0 if (JulianDate.is_leap_year(self.year) and
                       (self.month == JulianMonth.March) and
                       (self.event == Event.Kalends) and
                       (16 >= self.count >= 6))
                 else 1) +
                (1 if self.leap else 0))

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Roman name corresponding to fixed fixed_date 'fixed_date'."""
        julian_date = JulianDate.from_fixed(fixed_date)
        month_prime = amod(1 + julian_date.month, 12)
        year_prime  = (julian_date.year if month_prime != 1 
                       else (julian_date.year + 1 if (julian_date.year != -1) else 1))
        kalends1 = RomanDate(year_prime, month_prime, Event.Kalends, 1, False).to_fixed()
    
        if julian_date.day == 1:
            return RomanDate(julian_date.year, julian_date.month, Event.Kalends, 1, False)
        elif julian_date.day <= cls.nones_of_month(julian_date.month):
            return RomanDate(julian_date.year,
                             julian_date.month,
                             Event.Nones, 
                             cls.nones_of_month(julian_date.month) - julian_date.day + 1,
                             False)
        elif julian_date.day <= cls.ides_of_month(julian_date.month):
            return RomanDate(julian_date.year,
                             julian_date.month,
                             Event.Ides,
                             cls.ides_of_month(julian_date.month) - julian_date.day + 1,
                             False)
        elif (julian_date.month != JulianMonth.February) or not julian_date.is_leap_year(julian_date.year):
            return RomanDate(year_prime,
                             month_prime,
                             Event.Kalends,
                             kalends1 - fixed_date + 1,
                             False)
        elif julian_date.day < 25:
            return RomanDate(julian_date.year, JulianMonth.March, Event.Kalends, 30 - julian_date.day, False)
        else:
            return RomanDate(julian_date.year, JulianMonth.March, Event.Kalends, 31 - julian_date.day, julian_date.day == 25)

    




#######################################
# ecclesiastical calendars algorithms #
#######################################
# see lines 1371-1385 in calendrica-3.0.cl
def orthodox_easter(g_year):
    """Return fixed date of Orthodox Easter in Gregorian year g_year."""
    shifted_epact = mod(14 + 11 * mod(g_year, 19), 30)
    j_year        = g_year if g_year > 0 else g_year - 1
    paschal_moon  = JulianDate(j_year, JulianMonth.April, 19).to_fixed() - shifted_epact
    return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)

# see lines 76-91 in calendrica-3.0.errata.cl
def alt_orthodox_easter(g_year):
    """Return fixed date of Orthodox Easter in Gregorian year g_year.
    Alternative calculation."""
    paschal_moon = (354 * g_year +
                    30 * quotient((7 * g_year) + 8, 19) +
                    quotient(g_year, 4)  -
                    quotient(g_year, 19) -
                    273 +
                    GregorianDate.EPOCH)
    return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)

# see lines 1401-1426 in calendrica-3.0.cl
def easter(g_year):
    """Return fixed date of Easter in Gregorian year g_year."""
    century = quotient(g_year, 100) + 1
    shifted_epact = mod(14 +
                        11 * mod(g_year, 19) -
                        quotient(3 * century, 4) +
                        quotient(5 + (8 * century), 25), 30)
    adjusted_epact = ((shifted_epact + 1)
                      if ((shifted_epact == 0) or ((shifted_epact == 1) and
                                                  (10 < mod(g_year, 19))))
                      else  shifted_epact)
    paschal_moon = GregorianDate(g_year, JulianMonth.April, 19).to_fixed() - adjusted_epact
    return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)

# see lines 1429-1431 in calendrica-3.0.cl
def pentecost(g_year):
    """Return fixed date of Pentecost in Gregorian year g_year."""
    return easter(g_year) + 49






    





##################################
# old hindu calendars algorithms #
##################################
class OldHindu(object):
    
    ARYA_SOLAR_YEAR = 1577917500/4320000
    ARYA_SOLAR_MONTH = ARYA_SOLAR_YEAR / 12

    HINDU_EPOCH = JulianDate(JulianDate.bce(3102), JulianMonth.February, 18).to_fixed()

    @classmethod    
    def hindu_day_count(cls, date):
        """Return elapsed days (Ahargana) to date date since Hindu epoch (KY)."""
        return date - cls.HINDU_EPOCH

    # see lines 2462-2466 in calendrica-3.0.cl
    ARYA_JOVIAN_PERIOD =  1577917500/364224
    
    @classmethod
    def jovian_year(cls, date):
        """Return year of Jupiter cycle at fixed date date."""
        return amod(quotient(cls.hindu_day_count(date), cls.ARYA_JOVIAN_PERIOD / 12) + 27, 60)

class OldHinduLunarDate(OldHindu):
    
    ARYA_LUNAR_MONTH = 1577917500/53433336
    ARYA_LUNAR_DAY =  ARYA_LUNAR_MONTH / 30

    def __init__(self, year, month, leap, day):
        self.year = year
        self.month = month
        self.leap = leap
        self.day = day
        
    # see lines 2433-2460 in calendrica-3.0.cl
    def to_fixed(self):
        """Return fixed date corresponding to Old Hindu lunar date l_date."""
        mina  = ((12 * self.year) - 1) * self.ARYA_SOLAR_MONTH
        lunar_new_year = self.ARYA_LUNAR_MONTH * (quotient(mina, self.ARYA_LUNAR_MONTH) + 1)
    
        if ((not self.leap) and 
            (iceiling((lunar_new_year - mina) / (self.ARYA_SOLAR_MONTH - self.ARYA_LUNAR_MONTH))
             <= self.month)):
            temp = self.month
        else:
            temp = self.month - 1
        temp = (self.HINDU_EPOCH    + 
                lunar_new_year +
                (self.ARYA_LUNAR_MONTH * temp) +
                ((self.day - 1) * self.ARYA_LUNAR_DAY) +
                Clock.days_from_hours(-6))
        return iceiling(temp)

    @classmethod
    def is_leap_year(cls, l_year):
        """Return True if l_year is a leap year on the
        old Hindu calendar."""
        return mod(l_year * cls.ARYA_SOLAR_YEAR - cls.ARYA_SOLAR_MONTH,
                   cls.ARYA_LUNAR_MONTH) >= 23902504679/1282400064

    @classmethod
    def from_fixed(cls, date):
        """Return Old Hindu lunar date equivalent to fixed date date."""
        sun = cls.hindu_day_count(date) + Clock.days_from_hours(6)
        new_moon = sun - mod(sun, cls.ARYA_LUNAR_MONTH)
        leap = (((cls.ARYA_SOLAR_MONTH - cls.ARYA_LUNAR_MONTH)
                 >=
                 mod(new_moon, cls.ARYA_SOLAR_MONTH))
                and
                (mod(new_moon, cls.ARYA_SOLAR_MONTH) > 0))
        month = mod(iceiling(new_moon / cls.ARYA_SOLAR_MONTH), 12) + 1
        day = mod(quotient(sun, cls.ARYA_LUNAR_DAY), 30) + 1
        year = iceiling((new_moon + cls.ARYA_SOLAR_MONTH) / cls.ARYA_SOLAR_YEAR) - 1
        return OldHinduLunarDate(year, month, leap, day)

class OldHinduSolarDate(OldHindu):

    
    def __init(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_fixed(cls, date):
        """Return Old Hindu solar date equivalent to fixed date date."""
        sun   = cls.hindu_day_count(date) + Clock.days_from_hours(6)
        year  = quotient(sun, cls.ARYA_SOLAR_YEAR)
        month = mod(quotient(sun, cls.ARYA_SOLAR_MONTH), 12) + 1
        day   = ifloor(mod(sun, cls.ARYA_SOLAR_MONTH)) + 1
        return OldHinduSolarDate(year, month, day)
        
    def to_fixed(self):
        """Return fixed date corresponding to Old Hindu solar date s_date."""
        return iceiling(self.HINDU_EPOCH                 +
                    self.year * self.ARYA_SOLAR_YEAR         +
                    (self.month - 1) * self.ARYA_SOLAR_MONTH +
                    self.day + Clock.days_from_hours(-30))



######################
# Time and Astronomy #
######################

class ElipticalCoordinates(object):
    
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    @classmethod        
    def from_equatorial(cls, ra, declination, obliquity):
        """Convert equatorial coordinates (in degrees) to ecliptical ones.
        'declination' is the declination,
        'ra' is the right ascension and
        'obliquity' is the obliquity of the ecliptic.
        NOTE: if 'apparent' right ascension and declination are used, then 'true'
              obliquity should be input.
        """
        co = cos_degrees(obliquity)
        so = sin_degrees(obliquity)
        sa = sin_degrees(ra)
        longitude = normalized_degrees_from_radians(atan2(sa*co + tan_degrees(declination)*so, cos_degrees(ra)))
        latitude = arcsin_degrees(sin_degrees(declination)*co - cos_degrees(declination)*so*sa)
        return ElipticalCoordinates(longitude, latitude)

class EquatorialCoordinates(object):
    
    def __init__(self, ra, declination):
        self.ra = ra
        self.declination = declination

    @classmethod        
    def from_ecliptical(cls, longitude, latitude, obliquity):
        """Convert ecliptical coordinates (in degrees) to equatorial ones.
        'longitude' is the ecliptical longitude,
        'latitude'  is the ecliptical latitude and
        'obliquity' is the obliquity of the ecliptic.
        NOTE: resuting 'ra' and 'declination' will be referred to the same equinox
              as the one of input ecliptical longitude and latitude.
        """
        co = cos_degrees(obliquity)
        so = sin_degrees(obliquity)
        sl = sin_degrees(longitude)
        ra = normalized_degrees_from_radians(atan2(sl*co - tan_degrees(latitude)*so, cos_degrees(longitude)))
        dec = arcsin_degrees(sin_degrees(latitude)*co + cos_degrees(latitude)*so*sl)
        return EquatorialCoordinates(ra, dec)

class HorizontalCoordinates(object):
    
    def __init__(self, azimuth, altitude):
        self.azimuth = azimuth
        self.altitude = altitude

    @classmethod        
    def horizontal_from_equatorial(cls, H, declination, latitude):
        """Convert equatorial coordinates (in degrees) to horizontal ones.
        Return 'azimuth' and 'altitude'.
        'H'            is the local hour angle,
        'declination'  is the declination,
        'latitude'     is the observer's geographic latitude.
        NOTE: 'azimuth' is measured westward from the South.
        NOTE: This is not a good formula for using near the poles.
        """
        ch = cos_degrees(H)
        sl = sin_degrees(latitude)
        cl = cos_degrees(latitude)
        azimuth = normalized_degrees_from_radians(atan2(sin_degrees(H), ch * sl - tan_degrees(declination) * cl))
        altitude = arcsin_degrees(sl * sin_degrees(declination) + cl * cos_degrees(declination) * ch)
        return HorizontalCoordinates(azimuth, altitude)

    def to_equatorial(self, phi):
        """Convert equatorial coordinates (in degrees) to horizontal ones.
        Return 'local hour angle' and 'declination'.
        'A'   is the azimuth,
        'h'   is the altitude,
        'phi' is the observer's geographical latitude.
        NOTE: 'azimuth' is measured westward from the South.
        """
        H = normalized_degrees_from_radians(
                atan2(sin_degrees(self.azimuth), 
                      (cos_degrees(self.azimuth) * sin_degrees(phi) + 
                       tan_degrees(self.altitude) * cos_degrees(phi))))
        delta = arcsin_degrees(sin_degrees(phi) * sin_degrees(self.altitude) - 
                               cos_degrees(phi) * cos_degrees(self.altitude) * cos_degrees(self.azimuth))
        return [H, delta]

def julian_centuries(tee):
    """Return Julian centuries since 2000 at moment tee."""
    return (dynamical_from_universal(tee) - J2000) / mpf(36525)

def obliquity(tee):
    """Return (mean) obliquity of ecliptic at moment tee."""
    c = julian_centuries(tee)
    return (angle(23, 26, mpf(21.448)) +
            poly(c, [mpf(0),
                     angle(0, 0, mpf(-46.8150)),
                     angle(0, 0, mpf(-0.00059)),
                     angle(0, 0, mpf(0.001813))]))

def precise_obliquity(tee):
    """Return precise (mean) obliquity of ecliptic at moment tee."""
    u = julian_centuries(tee)/100
    #assert(abs(u) < 1,
    #       'Error! This formula is valid for +/-10000 years around J2000.0')
    return (poly(u, [angle(23, 26, mpf(21.448)),
                     angle(0, 0, mpf(-4680.93)),
                     angle(0, 0, mpf(-   1.55)),
                     angle(0, 0, mpf(+1999.25)),
                     angle(0, 0, mpf(-  51.38)),
                     angle(0, 0, mpf(- 249.67)),
                     angle(0, 0, mpf(-  39.05)),
                     angle(0, 0, mpf(+   7.12)),
                     angle(0, 0, mpf(+  27.87)),
                     angle(0, 0, mpf(+   5.79)),
                     angle(0, 0, mpf(+   2.45))]))

def declination(tee, beta, lam):
    """Return declination at moment UT tee of object at
    longitude 'lam' and latitude 'beta'."""
    varepsilon = obliquity(tee)
    return arcsin_degrees(
        (sin_degrees(beta) * cos_degrees(varepsilon)) +
        (cos_degrees(beta) * sin_degrees(varepsilon) * sin_degrees(lam)))

def right_ascension(tee, beta, lam):
    """Return right ascension at moment UT 'tee' of object at
    latitude 'lam' and longitude 'beta'."""
    varepsilon = obliquity(tee)
    return arctan_degrees((sin_degrees(lam) * cos_degrees(varepsilon)) - (tan_degrees(beta) * sin_degrees(varepsilon)), cos_degrees(lam))

class Location(object):

    MORNING = True
    EVENING = False
    
    def __init__(self, latitude, longitude, elevation, zone):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.zone = zone

    def direction(self, focus):
        """Return the angle (clockwise from North) to face focus when
        standing in location, location.  Subject to errors near focus and
        its antipode."""
        phi = self.latitude
        phi_prime = focus.latitude
        psi = self.longitude
        psi_prime = focus.longitude
        y = sin_degrees(psi_prime - psi)
        x = ((cos_degrees(phi) * tan_degrees(phi_prime)) -
             (sin_degrees(phi)    * cos_degrees(psi - psi_prime)))
        if ((x == y == 0) or (phi_prime == 90)):
            return 0
        elif (phi_prime == -90):
            return 180
        else:
            return arctan_degrees(y, x)

    def standard_from_universal(self, tee_rom_u):
        """Return standard time from tee_rom_u in universal time at location."""
        return tee_rom_u + self.zone
    
    # see lines 2805-2809 in calendrica-3.0.cl
    def universal_from_standard(self, tee_rom_s):
        """Return universal time from tee_rom_s in standard time at location."""
        return tee_rom_s - self.zone

    @classmethod
    def zone_from_longitude(cls, phi):
        """Return the difference between UT and local mean time at longitude
        'phi' as a fraction of a day."""
        return phi / 360
    
    def local_from_universal(self, tee_rom_u):
        """Return local time from universal tee_rom_u at location, location."""
        return tee_rom_u + self.zone_from_longitude(self.longitude)
    
    def universal_from_local(self, tee_ell):
        """Return universal time from local tee_ell at location, location."""
        return tee_ell - self.zone_from_longitude(self.longitude)
    
    def standard_from_local(self, tee_ell):
        """Return standard time from local tee_ell at locale, location."""
        return self.standard_from_universal(self.universal_from_local(tee_ell))
    
    def local_from_standard(self, tee_rom_s):
        """Return local time from standard tee_rom_s at location, location."""
        return self.local_from_universal(self.universal_from_standard(tee_rom_s))
    
    # see lines 2841-2844 in calendrica-3.0.cl
    def apparent_from_local(self, tee):
        """Return sundial time at local time tee at location, location."""
        return tee + equation_of_time(self.universal_from_local(tee))
    
    # see lines 2846-2849 in calendrica-3.0.cl
    def local_from_apparent(self, tee):
        """Return local time from sundial time tee at location, location."""
        return tee - equation_of_time(self.universal_from_local(tee))
    
    # see lines 2851-2857 in calendrica-3.0.cl
    def midnight(self, date):
        """Return standard time on fixed date, date, of true (apparent)
        midnight at location, location."""
        return self.standard_from_local(self.local_from_apparent(date))
    
    # see lines 2859-2864 in calendrica-3.0.cl
    def midday(self, date):
        """Return standard time on fixed date, date, of midday
        at location, location."""
        return self.standard_from_local(self.local_from_apparent(date + Clock.days_from_hours(mpf(12))))

    def sine_offset(self, tee, alpha):
        """Return sine of angle between position of sun at 
        local time tee and when its depression is alpha at location, location.
        Out of range when it does not occur."""
        phi = self.latitude
        tee_prime = self.universal_from_local(tee)
        delta = declination(tee_prime, mpf(0), solar_longitude(tee_prime))
        return ((tan_degrees(phi) * tan_degrees(delta)) +
                (sin_degrees(alpha) / (cos_degrees(delta) *
                                       cos_degrees(phi))))

    # see lines 2922-2947 in calendrica-3.0.cl
    def approx_moment_of_depression(self, tee, alpha, early):
        """Return the moment in local time near tee when depression angle
        of sun is alpha (negative if above horizon) at location;
        early is true when MORNING event is sought and false for EVENING.
        Raise VlueError if depression angle is not reached."""
        ttry  = self.sine_offset(tee, alpha)
        date = Clock.fixed_from_moment(tee)
    
        if (alpha >= 0):
            if early:
                alt = date
            else:
                alt = date + 1
        else:
            alt = date + Clock.days_from_hours(12)
    
        if (abs(ttry) > 1):
            value = self.sine_offset(alt, alpha)
        else:
            value = ttry
    
    
        if (abs(value) <= 1):
            temp = -1 if early else 1
            temp *= mod(Clock.days_from_hours(12) + arcsin_degrees(value) / 360, 1) - Clock.days_from_hours(6)
            temp += date + Clock.days_from_hours(12)
            return self.local_from_apparent(temp)
        else:
            raise ValueError("Depression angle not reached")

    def moment_of_depression(self, approx, alpha, early):
        """Return the moment in local time near approx when depression
        angle of sun is alpha (negative if above horizon) at location;
        early is true when MORNING event is sought, and false for EVENING."""
        tee = self.approx_moment_of_depression(approx, alpha, early)
        if abs(approx - tee) < Clock.days_from_seconds(30):
            return tee
        else:
            return self.moment_of_depression(tee, alpha, early)

    def dawn(self, date, alpha):
        """Return standard time in morning on fixed date date at
        location location when depression angle of sun is alpha."""
        result = self.moment_of_depression(date + Clock.days_from_hours(6), alpha, self.MORNING)
        return self.standard_from_local(result)
    
    def dusk(self, date, alpha):
        """Return standard time in evening on fixed date 'date' at
        location 'location' when depression angle of sun is alpha."""
        result = self.moment_of_depression(date + Clock.days_from_hours(18), alpha, self.EVENING)
        return self.standard_from_local(result)

    def refraction(self, tee):
        """Return refraction angle at location 'location' and time 'tee'."""
        h     = max(0, self.elevation)
        cap_R = 6.372E6
        dip   = arccos_degrees(cap_R / (cap_R + h))
        return angle(0, 50, 0) + dip + secs(19) * math.sqrt(h)

    def sunrise(self, date):
        """Return Standard time of sunrise on fixed date 'date' at
        location 'location'."""
        alpha = self.refraction(date)
        return self.dawn(date, alpha)
    
    def sunset(self, date):
        """Return standard time of sunset on fixed date 'date' at
        location 'location'."""
        alpha = self.refraction(date)
        return self.dusk(date, alpha)
    
    def observed_lunar_altitude(self, tee):
        """Return the observed altitude of moon at moment, tee, and
        at location, location,  taking refraction into account."""
        return self.topocentric_lunar_altitude(tee) + self.refraction(tee)
    
    def moonrise(self, date):
        """Return the standard time of moonrise on fixed, date,
        and location, location."""
        t = self.universal_from_standard(date)
        waning = (lunar_phase(t) > 180)
        alt = self.observed_lunar_altitude(t)
        offset = alt / 360
        if (waning and (offset > 0)):
            approx =  t + 1 - offset
        elif waning:
            approx = t - offset
        else:
            approx = t + (1 / 2) + offset
        rise = binary_search(approx - Clock.days_from_hours(3),
                             approx + Clock.days_from_hours(3),
                             lambda u, l: ((u - l) < Clock.days_from_hours(1 / 60)),
                             lambda x: self.observed_lunar_altitude(x) > 0)
        if (rise < (t + 1)):
            return self.standard_from_universal(rise)
        
        raise ValueError()

    def daytime_temporal_hour(self, date):
        """Return the length of daytime temporal hour on fixed date, date
        at location, location."""
        return (self.sunset(date) - self.sunrise(date)) / 12
    
    def nighttime_temporal_hour(self, date):
        """Return the length of nighttime temporal hour on fixed date, date,
        at location, location."""
        return (self.sunrise(date + 1) - self.sunset(date)) / 12

MECCA = Location(angle(21, 25, 24), angle(39, 49, 24), 298, Clock.days_from_hours(3))
JERUSALEM = Location(31.8, 35.2, 800, Clock.days_from_hours(2))
BRUXELLES = Location(angle(4, 21, 17), angle(50, 50, 47), 800, Clock.days_from_hours(1))
URBANA = Location(40.1, -88.2, 225, Clock.days_from_hours(-6))
GREENWHICH = Location(51.4777815, 0, 46.9, Clock.days_from_hours(0))

def urbana_sunset(gdate):
    """Return sunset time in Urbana, Ill, on Gregorian date 'gdate'."""
    return Clock.time_from_moment(URBANA.sunset(gdate.to_fixed()))

def urbana_winter(g_year):
    """Return standard time of the winter solstice in Urbana, Illinois, USA."""
    return URBANA.standard_from_universal(solar_longitude_after(WINTER, GregorianDate(g_year, JulianMonth.January, 1).to_fixed()))

###########################################
# astronomical lunar calendars algorithms #
###########################################
# see lines 3021-3025 in calendrica-3.0.cl
def jewish_dusk(date, location):
    """Return standard time of Jewish dusk on fixed date, date,
    at location, location, (as per Vilna Gaon)."""
    return location.dusk(date, angle(4, 40, 0))

# see lines 3027-3031 in calendrica-3.0.cl
def jewish_sabbath_ends(date, location):
    """Return standard time of end of Jewish sabbath on fixed date, date,
    at location, location, (as per Berthold Cohn)."""
    return location.dusk(date, angle(7, 5, 0)) 

# see lines 3055-3073 in calendrica-3.0.cl
def standard_from_sundial(tee, location):
    """Return standard time of temporal moment, tee, at location, location."""
    date = Clock.fixed_from_moment(tee)
    hour = 24 * mod(tee, 1)
    if (6 <= hour <= 18):
        h = location.daytime_temporal_hour(date)
    elif (hour < 6):
        h = location.nighttime_temporal_hour(date - 1)
    else:
        h = location.nighttime_temporal_hour(date)

    # return
    if (6 <= hour <= 18):
        return location.sunrise(date) + ((hour - 6) * h)
    elif (hour < 6):
        return location.sunset(date - 1) + ((hour + 6) * h)
    else:
        return location.sunset(date) + ((hour - 18) * h)


def jewish_morning_end(date, location):
    """Return standard time on fixed date, date, at location, location,
    of end of morning according to Jewish ritual."""
    return standard_from_sundial(date + Clock.days_from_hours(10), location)

def asr(date, location):
    """Return standard time of asr on fixed date, date,
    at location, location."""
    noon = location.universal_from_standard(location.midday(date))
    phi = location.latitude
    delta = declination(noon, 0, solar_longitude(noon))
    altitude = delta - phi - 90
    h = arctan_degrees(tan_degrees(altitude), 2 * tan_degrees(altitude) + 1)
    # For Shafii use instead:
    # tan_degrees(altitude) + 1)
    return location.dusk(date, -h)

############ here start the code inspired by Meeus
def universal_from_dynamical(tee):
    """Return Universal moment from Dynamical time, tee."""
    return tee - ephemeris_correction(tee)

def dynamical_from_universal(tee):
    """Return Dynamical time at Universal moment, tee."""
    return tee + ephemeris_correction(tee)

J2000 = Clock.days_from_hours(mpf(12)) + GregorianDate.new_year(2000)

def sidereal_from_moment(tee):
    """Return the mean sidereal time of day from moment tee expressed
    as hour angle.  Adapted from "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 1991."""
    c = (tee - J2000) / mpf(36525)
    return mod(poly(c, [mpf(280.46061837), mpf(36525) * mpf(360.98564736629), mpf(0.000387933), mpf(-1)/mpf(38710000)]), 360)

MEAN_TROPICAL_YEAR = mpf(365.242189)
MEAN_SIDEREAL_YEAR = mpf(365.25636)
MEAN_SYNODIC_MONTH = mpf(29.530588861)

def ephemeris_correction(tee):
    """Return Dynamical Time minus Universal Time (in days) for
    moment, tee.  Adapted from "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 1991."""
    year = GregorianDate.to_year(ifloor(tee))
    c = GregorianDate.date_difference(GregorianDate(1900, JulianMonth.January, 1), GregorianDate(year, JulianMonth.July, 1)) / mpf(36525)
    if (1988 <= year <= 2019):
        return 1/86400 * (year - 1933)
    elif (1900 <= year <= 1987):
        return poly(c, [mpf(-0.00002), mpf(0.000297), mpf(0.025184), mpf(-0.181133), mpf(0.553040), mpf(-0.861938), mpf(0.677066), mpf(-0.212591)])
    elif (1800 <= year <= 1899):
        return poly(c, [mpf(-0.000009), mpf(0.003844), mpf(0.083563), mpf(0.865736), mpf(4.867575), mpf(15.845535), mpf(31.332267), mpf(38.291999), mpf(28.316289), mpf(11.636204), mpf(2.043794)])
    elif (1700 <= year <= 1799):
        return (1/86400 * poly(year - 1700, [8.118780842, -0.005092142, 0.003336121, -0.0000266484]))
    elif (1620 <= year <= 1699):
        return (1/86400 * poly(year - 1600, [mpf(196.58333), mpf(-4.0675), mpf(0.0219167)]))
    else:
        x = (Clock.days_from_hours(mpf(12)) + GregorianDate.date_difference(GregorianDate(1810, JulianMonth.January, 1), GregorianDate(year, JulianMonth.January, 1)))
        return 1/86400 * (((x * x) / mpf(41048480)) - 15)

def equation_of_time(tee):
    """Return the equation of time (as fraction of day) for moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 1991."""
    c = julian_centuries(tee)
    lamb = poly(c, [mpf(280.46645), mpf(36000.76983), mpf(0.0003032)])
    anomaly = poly(c, [mpf(357.52910), mpf(35999.05030), mpf(-0.0001559), mpf(-0.00000048)])
    eccentricity = poly(c, [mpf(0.016708617), mpf(-0.000042037), mpf(-0.0000001236)])
    varepsilon = obliquity(tee)
    y = pow(tan_degrees(varepsilon / 2), 2)
    equation = ((1/2 / pi) *
                (y * sin_degrees(2 * lamb) +
                 -2 * eccentricity * sin_degrees(anomaly) +
                 (4 * eccentricity * y * sin_degrees(anomaly) *
                  cos_degrees(2 * lamb)) +
                 -0.5 * y * y * sin_degrees(4 * lamb) +
                 -1.25 * eccentricity * eccentricity * sin_degrees(2 * anomaly)))
    return signum(equation) * min(abs(equation), Clock.days_from_hours(mpf(12)))

# see lines 3209-3259 in calendrica-3.0.cl
def solar_longitude(tee):
    """Return the longitude of sun at moment 'tee'.
    Adapted from 'Planetary Programs and Tables from -4000 to +2800'
    by Pierre Bretagnon and Jean_Louis Simon, Willmann_Bell, Inc., 1986.
    See also pag 166 of 'Astronomical Algorithms' by Jean Meeus, 2nd Ed 1998,
    with corrections Jun 2005."""
    c = julian_centuries(tee)
    coefficients = [403406, 195207, 119433, 112392, 3891, 2819, 1721,
                    660, 350, 334, 314, 268, 242, 234, 158, 132, 129, 114,
                    99, 93, 86, 78,72, 68, 64, 46, 38, 37, 32, 29, 28, 27, 27,
                    25, 24, 21, 21, 20, 18, 17, 14, 13, 13, 13, 12, 10, 10, 10,
                    10]
    multipliers = [mpf(0.9287892), mpf(35999.1376958), mpf(35999.4089666),
                   mpf(35998.7287385), mpf(71998.20261), mpf(71998.4403),
                   mpf(36000.35726), mpf(71997.4812), mpf(32964.4678),
                   mpf(-19.4410), mpf(445267.1117), mpf(45036.8840), mpf(3.1008),
                   mpf(22518.4434), mpf(-19.9739), mpf(65928.9345),
                   mpf(9038.0293), mpf(3034.7684), mpf(33718.148), mpf(3034.448),
                   mpf(-2280.773), mpf(29929.992), mpf(31556.493), mpf(149.588),
                   mpf(9037.750), mpf(107997.405), mpf(-4444.176), mpf(151.771),
                   mpf(67555.316), mpf(31556.080), mpf(-4561.540),
                   mpf(107996.706), mpf(1221.655), mpf(62894.167),
                   mpf(31437.369), mpf(14578.298), mpf(-31931.757),
                   mpf(34777.243), mpf(1221.999), mpf(62894.511),
                   mpf(-4442.039), mpf(107997.909), mpf(119.066), mpf(16859.071),
                   mpf(-4.578), mpf(26895.292), mpf(-39.127), mpf(12297.536),
                   mpf(90073.778)]
    addends = [mpf(270.54861), mpf(340.19128), mpf(63.91854), mpf(331.26220),
               mpf(317.843), mpf(86.631), mpf(240.052), mpf(310.26), mpf(247.23),
               mpf(260.87), mpf(297.82), mpf(343.14), mpf(166.79), mpf(81.53),
               mpf(3.50), mpf(132.75), mpf(182.95), mpf(162.03), mpf(29.8),
               mpf(266.4), mpf(249.2), mpf(157.6), mpf(257.8),mpf(185.1),
               mpf(69.9),  mpf(8.0), mpf(197.1), mpf(250.4), mpf(65.3),
               mpf(162.7), mpf(341.5), mpf(291.6), mpf(98.5), mpf(146.7),
               mpf(110.0), mpf(5.2), mpf(342.6), mpf(230.9), mpf(256.1),
               mpf(45.3), mpf(242.9), mpf(115.2), mpf(151.8), mpf(285.3),
               mpf(53.3), mpf(126.6), mpf(205.7), mpf(85.9), mpf(146.1)]
    lam = (mpf(282.7771834) +
           mpf(36000.76953744) * c +
           mpf(0.000005729577951308232) *
           sigma([coefficients, addends, multipliers],
                 lambda x, y, z:  x * sin_degrees(y + (z * c))))
    return mod(lam + aberration(tee) + nutation(tee), 360)

def geometric_solar_mean_longitude(tee):
    """Return the geometric mean longitude of the Sun at moment, tee,
    referred to mean equinox of the date."""
    c = julian_centuries(tee)
    return poly(c, [mpf(280.46646), mpf(36000.76983), mpf(0.0003032)])

def solar_latitude(tee):
    """Return the latitude of Sun (in degrees) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 1998."""
    pass

def solar_distance(tee):
    """Return the distance of Sun (in degrees) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 1998."""
    pass

def solar_position(tee):
    """Return the position of the Sun (geocentric latitude and longitude [in degrees]
    and distance [in meters]) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed."""
    return (solar_latitude(tee), solar_longitude(tee), solar_distance(tee))


# see lines 3261-3271 in calendrica-3.0.cl
def nutation(tee):
    """Return the longitudinal nutation at moment, tee."""
    c = julian_centuries(tee)
    cap_A = poly(c, [mpf(124.90), mpf(-1934.134), mpf(0.002063)])
    cap_B = poly(c, [mpf(201.11), mpf(72001.5377), mpf(0.00057)])
    return (mpf(-0.004778)  * sin_degrees(cap_A) + 
            mpf(-0.0003667) * sin_degrees(cap_B))

# see lines 3273-3281 in calendrica-3.0.cl
def aberration(tee):
    """Return the aberration at moment, tee."""
    c = julian_centuries(tee)
    return ((mpf(0.0000974) *
             cos_degrees(mpf(177.63) + mpf(35999.01848) * c)) -
            mpf(0.005575))

# see lines 3283-3295 in calendrica-3.0.cl
def solar_longitude_after(lam, tee):
    """Return the moment UT of the first time at or after moment, tee,
    when the solar longitude will be lam degrees."""
    rate = MEAN_TROPICAL_YEAR / 360
    tau = tee + rate * mod(lam - solar_longitude(tee), 360)
    a = max(tee, tau - 5)
    b = tau + 5
    return invert_angular(solar_longitude, lam, a, b)

SPRING = 0
SUMMER = 90
AUTUMN = 180
WINTER = 270

# see lines 3317-3339 in calendrica-3.0.cl
def precession(tee):
    """Return the precession at moment tee using 0,0 as J2000 coordinates.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann-Bell, Inc., 1991."""
    c = julian_centuries(tee)
    eta = mod(poly(c, [0,
                       secs(mpf(47.0029)),
                       secs(mpf(-0.03302)),
                       secs(mpf(0.000060))]),
              360)
    cap_P = mod(poly(c, [mpf(174.876384), 
                         secs(mpf(-869.8089)), 
                         secs(mpf(0.03536))]),
                360)
    p = mod(poly(c, [0,
                     secs(mpf(5029.0966)),
                     secs(mpf(1.11113)),
                     secs(mpf(0.000006))]),
            360)
    cap_A = cos_degrees(eta) * sin_degrees(cap_P)
    cap_B = cos_degrees(cap_P)
    arg = arctan_degrees(cap_A, cap_B)

    return mod(p + cap_P - arg, 360)

# see lines 3341-3347 in calendrica-3.0.cl
def sidereal_solar_longitude(tee):
    """Return sidereal solar longitude at moment, tee."""
    return mod(solar_longitude(tee) - precession(tee) + SIDEREAL_START, 360)

# see lines 3349-3365 in calendrica-3.0.cl
def estimate_prior_solar_longitude(lam, tee):
    """Return approximate moment at or before tee
    when solar longitude just exceeded lam degrees."""
    rate = MEAN_TROPICAL_YEAR / 360
    tau = tee - (rate * mod(solar_longitude(tee) - lam, 360))
    cap_Delta = mod(solar_longitude(tau) - lam + 180, 360) - 180
    return min(tee, tau - (rate * cap_Delta))

# see lines 3367-3376 in calendrica-3.0.cl
def mean_lunar_longitude(c):
    """Return mean longitude of moon (in degrees) at moment
    given in Julian centuries c (including the constant term of the
    effect of the light-time (-0".70).
    Adapted from eq. 47.1 in "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
    return normalized_degrees(poly(c, [mpf(218.3164477), mpf(481267.88123421),
                               mpf(-0.0015786), mpf(1/538841),
                               mpf(-1/65194000)]))

# see lines 3378-3387 in calendrica-3.0.cl
def lunar_elongation(c):
    """Return elongation of moon (in degrees) at moment
    given in Julian centuries c.
    Adapted from eq. 47.2 in "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
    return normalized_degrees(poly(c, [mpf(297.8501921), mpf(445267.1114034),
                                mpf(-0.0018819), mpf(1/545868),
                                mpf(-1/113065000)]))

# see lines 3389-3398 in calendrica-3.0.cl
def solar_anomaly(c):
    """Return mean anomaly of sun (in degrees) at moment
    given in Julian centuries c.
    Adapted from eq. 47.3 in "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
    return normalized_degrees(poly(c, [mpf(357.5291092), mpf(35999.0502909), mpf(-0.0001536), mpf(1/24490000)]))

# see lines 3400-3409 in calendrica-3.0.cl
def lunar_anomaly(c):
    """Return mean anomaly of moon (in degrees) at moment
    given in Julian centuries c.
    Adapted from eq. 47.4 in "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
    return normalized_degrees(poly(c, [mpf(134.9633964), mpf(477198.8675055), mpf(0.0087414), mpf(1/69699), mpf(-1/14712000)]))


# see lines 3411-3420 in calendrica-3.0.cl
def moon_node(c):
    """Return Moon's argument of latitude (in degrees) at moment
    given in Julian centuries 'c'.
    Adapted from eq. 47.5 in "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
    return normalized_degrees(poly(c, [mpf(93.2720950), mpf(483202.0175233), mpf(-0.0036539), mpf(-1/3526000), mpf(1/863310000)]))

# see lines 3422-3485 in calendrica-3.0.cl
def lunar_longitude(tee):
    """Return longitude of moon (in degrees) at moment tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed., 1998."""
    c = julian_centuries(tee)
    cap_L_prime = mean_lunar_longitude(c)
    cap_D = lunar_elongation(c)
    cap_M = solar_anomaly(c)
    cap_M_prime = lunar_anomaly(c)
    cap_F = moon_node(c)
    # see eq. 47.6 in Meeus
    cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
    args_lunar_elongation = \
            [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1,
             1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2,
             2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2]
    args_solar_anomaly = \
            [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
             0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1,
             -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0]
    args_lunar_anomaly = \
            [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2,
             -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0,
             -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3,
             2, 1, -1, 3]
    args_moon_node = \
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0,
             0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0]
    sine_coefficients = \
            [6288774,1274027,658314,213618,-185116,-114332,
             58793,57066,53322,45758,-40923,-34720,-30383,
             15327,-12528,10980,10675,10034,8548,-7888,
             -6766,-5163,4987,4036,3994,3861,3665,-2689,
             -2602, 2390,-2348,2236,-2120,-2069,2048,-1773,
             -1595,1215,-1110,-892,-810,759,-713,-700,691,
             596,549,537,520,-487,-399,-381,351,-340,330,
             327,-323,299,294]
    correction = ((1/1000000) *
                  sigma([sine_coefficients, args_lunar_elongation,
                         args_solar_anomaly, args_lunar_anomaly,
                         args_moon_node],
                        lambda v, w, x, y, z:
                        v * pow(cap_E, abs(x)) *
                        sin_degrees((w * cap_D) +
                                    (x * cap_M) +
                                    (y * cap_M_prime) +
                                    (z * cap_F))))
    A1 = mpf(119.75) + (c * mpf(131.849))
    venus = ((3958/1000000) * sin_degrees(A1))
    A2 = mpf(53.09) + c * mpf(479264.29)
    jupiter = ((318/1000000) * sin_degrees(A2))
    flat_earth = ((1962/1000000) * sin_degrees(cap_L_prime - cap_F))

    return mod(cap_L_prime + correction + venus +
               jupiter + flat_earth + nutation(tee), 360)

# see lines 3663-3732 in calendrica-3.0.cl
def lunar_latitude(tee):
    """Return the latitude of moon (in degrees) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 1998."""
    c = julian_centuries(tee)
    cap_L_prime = mean_lunar_longitude(c)
    cap_D = lunar_elongation(c)
    cap_M = solar_anomaly(c)
    cap_M_prime = lunar_anomaly(c)
    cap_F = moon_node(c)
    cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
    args_lunar_elongation = \
            [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 4, 0, 0, 0,
             1, 0, 0, 0, 1, 0, 4, 4, 0, 4, 2, 2, 2, 2, 0, 2, 2, 2, 2, 4, 2, 2,
             0, 2, 1, 1, 0, 2, 1, 2, 0, 4, 4, 1, 4, 1, 4, 2]
    args_solar_anomaly = \
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, -1, -1, -1, 1, 0, 1,
             0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 1,
             0, -1, -2, 0, 1, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0, 0, -1, -2]
    args_lunar_anomaly = \
            [0, 1, 1, 0, -1, -1, 0, 2, 1, 2, 0, -2, 1, 0, -1, 0, -1, -1, -1,
             0, 0, -1, 0, 1, 1, 0, 0, 3, 0, -1, 1, -2, 0, 2, 1, -2, 3, 2, -3,
             -1, 0, 0, 1, 0, 1, 1, 0, 0, -2, -1, 1, -2, 2, -2, -1, 1, 1, -2,
             0, 0]
    args_moon_node = \
            [1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1,
             -1, 1, 3, 1, 1, 1, -1, -1, -1, 1, -1, 1, -3, 1, -3, -1, -1, 1,
             -1, 1, -1, 1, 1, 1, 1, -1, 3, -1, -1, 1, -1, -1, 1, -1, 1, -1,
             -1, -1, -1, -1, -1, 1]
    sine_coefficients = \
            [5128122, 280602, 277693, 173237, 55413, 46271, 32573,
             17198, 9266, 8822, 8216, 4324, 4200, -3359, 2463, 2211,
             2065, -1870, 1828, -1794, -1749, -1565, -1491, -1475,
             -1410, -1344, -1335, 1107, 1021, 833, 777, 671, 607,
             596, 491, -451, 439, 422, 421, -366, -351, 331, 315,
             302, -283, -229, 223, 223, -220, -220, -185, 181,
             -177, 176, 166, -164, 132, -119, 115, 107]
    beta = ((1/1000000) *
            sigma([sine_coefficients, 
                   args_lunar_elongation,
                   args_solar_anomaly,
                   args_lunar_anomaly,
                   args_moon_node],
                  lambda v, w, x, y, z: (v *
                                         pow(cap_E, abs(x)) *
                                         sin_degrees((w * cap_D) +
                                                     (x * cap_M) +
                                                     (y * cap_M_prime) +
                                                     (z * cap_F)))))
    venus = ((175/1000000) *
             (sin_degrees(mpf(119.75) + c * mpf(131.849) + cap_F) +
              sin_degrees(mpf(119.75) + c * mpf(131.849) - cap_F)))
    flat_earth = ((-2235/1000000) *  sin_degrees(cap_L_prime) +
                  (127/1000000) * sin_degrees(cap_L_prime - cap_M_prime) +
                  (-115/1000000) * sin_degrees(cap_L_prime + cap_M_prime))
    extra = ((382/1000000) *
             sin_degrees(mpf(313.45) + c * mpf(481266.484)))
    return beta + venus + flat_earth + extra


# see lines 192-197 in calendrica-3.0.errata.cl
def lunar_node(tee):
    """Return Angular distance of the node from the equinoctal point
    at fixed moment, tee.
    Adapted from eq. 47.7 in "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
    with corrections June 2005."""
    return mod(moon_node(julian_centuries(tee)) + 90, 180) - 90

def alt_lunar_node(tee):
    """Return Angular distance of the node from the equinoctal point
    at fixed moment, tee.
    Adapted from eq. 47.7 in "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
    with corrections June 2005."""
    return normalized_degrees(poly(julian_centuries(tee), [mpf(125.0445479), mpf(-1934.1362891), mpf(0.0020754), mpf(1/467441), mpf(-1/60616000)]))

def lunar_true_node(tee):
    """Return Angular distance of the true node (the node of the instantaneus
    lunar orbit) from the equinoctal point at moment, tee.
    Adapted from eq. 47.7 and pag. 344 in "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
    with corrections June 2005."""
    c = julian_centuries(tee)
    cap_D = lunar_elongation(c)
    cap_M = solar_anomaly(c)
    cap_M_prime = lunar_anomaly(c)
    cap_F = moon_node(c)
    periodic_terms = (-1.4979 * sin_degrees(2 * (cap_D - cap_F)) +
                      -0.1500 * sin_degrees(cap_M) +
                      -0.1226 * sin_degrees(2 * cap_D) +
                      0.1176  * sin_degrees(2 * cap_F) +
                      -0.0801 * sin_degrees(2 * (cap_M_prime - cap_F)))
    return alt_lunar_node(tee) + periodic_terms

def lunar_perigee(tee):
    """Return Angular distance of the perigee from the equinoctal point
    at moment, tee.
    Adapted from eq. 47.7 in "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
    with corrections June 2005."""
    return normalized_degrees(poly(julian_centuries(tee), [mpf(83.3532465), mpf(4069.0137287), mpf(-0.0103200), mpf(-1/80053), mpf(1/18999000)]))


# see lines 199-206 in calendrica-3.0.errata.cl
def sidereal_lunar_longitude(tee):
    """Return sidereal lunar longitude at moment, tee."""
    return mod(lunar_longitude(tee) - precession(tee) + SIDEREAL_START, 360)


# see lines 99-190 in calendrica-3.0.errata.cl
def nth_new_moon(n):
    """Return the moment of n-th new moon after (or before) the new moon
    of January 11, 1.  Adapted from "Astronomical Algorithms"
    by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998."""
    n0 = 24724
    k = n - n0
    c = k / mpf(1236.85)
    approx = (J2000 +
              poly(c, [mpf(5.09766),
                       MEAN_SYNODIC_MONTH * mpf(1236.85),
                       mpf(0.0001437),
                       mpf(-0.000000150),
                       mpf(0.00000000073)]))
    cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
    solar_anomaly = poly(c, [mpf(2.5534), (mpf(1236.85) * mpf(29.10535669)), mpf(-0.0000014), mpf(-0.00000011)])
    lunar_anomaly = poly(c, [mpf(201.5643), (mpf(385.81693528) * mpf(1236.85)), mpf(0.0107582), mpf(0.00001238), mpf(-0.000000058)])
    moon_argument = poly(c, [mpf(160.7108), (mpf(390.67050284) * mpf(1236.85)), mpf(-0.0016118), mpf(-0.00000227), mpf(0.000000011)])
    cap_omega = poly(c, [mpf(124.7746), (mpf(-1.56375588) * mpf(1236.85)), mpf(0.0020672), mpf(0.00000215)])
    E_factor = [0, 1, 0, 0, 1, 1, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0]
    solar_coeff = [0, 1, 0, 0, -1, 1, 2, 0, 0, 1, 0, 1, 1, -1, 2,
                   0, 3, 1, 0, 1, -1, -1, 1, 0]
    lunar_coeff = [1, 0, 2, 0, 1, 1, 0, 1, 1, 2, 3, 0, 0, 2, 1, 2,
                   0, 1, 2, 1, 1, 1, 3, 4]
    moon_coeff = [0, 0, 0, 2, 0, 0, 0, -2, 2, 0, 0, 2, -2, 0, 0,
                  -2, 0, -2, 2, 2, 2, -2, 0, 0]
    sine_coeff = [mpf(-0.40720), mpf(0.17241), mpf(0.01608),
                  mpf(0.01039),  mpf(0.00739), mpf(-0.00514),
                  mpf(0.00208), mpf(-0.00111), mpf(-0.00057),
                  mpf(0.00056), mpf(-0.00042), mpf(0.00042),
                  mpf(0.00038), mpf(-0.00024), mpf(-0.00007),
                  mpf(0.00004), mpf(0.00004), mpf(0.00003),
                  mpf(0.00003), mpf(-0.00003), mpf(0.00003),
                  mpf(-0.00002), mpf(-0.00002), mpf(0.00002)]
    correction = ((mpf(-0.00017) * sin_degrees(cap_omega)) +
                  sigma([sine_coeff, E_factor, solar_coeff,
                         lunar_coeff, moon_coeff],
                        lambda v, w, x, y, z: (v *
                                    pow(cap_E, w) *
                                    sin_degrees((x * solar_anomaly) + 
                                                (y * lunar_anomaly) +
                                                (z * moon_argument)))))
    add_const = [mpf(251.88), mpf(251.83), mpf(349.42), mpf(84.66),
                 mpf(141.74), mpf(207.14), mpf(154.84), mpf(34.52),
                 mpf(207.19), mpf(291.34), mpf(161.72), mpf(239.56),
                 mpf(331.55)]
    add_coeff = [mpf(0.016321), mpf(26.651886), mpf(36.412478),
                 mpf(18.206239), mpf(53.303771), mpf(2.453732),
                 mpf(7.306860), mpf(27.261239), mpf(0.121824),
                 mpf(1.844379), mpf(24.198154), mpf(25.513099),
                 mpf(3.592518)]
    add_factor = [mpf(0.000165), mpf(0.000164), mpf(0.000126),
                  mpf(0.000110), mpf(0.000062), mpf(0.000060),
                  mpf(0.000056), mpf(0.000047), mpf(0.000042),
                  mpf(0.000040), mpf(0.000037), mpf(0.000035),
                  mpf(0.000023)]
    extra = (mpf(0.000325) * sin_degrees(poly(c, [mpf(299.77), mpf(132.8475848), mpf(-0.009173)])))
    additional = sigma([add_const, add_coeff, add_factor],
                       lambda i, j, l: l * sin_degrees(i + j * k))

    return universal_from_dynamical(approx + correction + extra + additional)


# see lines 3578-3585 in calendrica-3.0.cl
def new_moon_before(tee):
    """Return the moment UT of last new moon before moment tee."""
    t0 = nth_new_moon(0)
    phi = lunar_phase(tee)
    n = iround(((tee - t0) / MEAN_SYNODIC_MONTH) - (phi / 360))
    return nth_new_moon(final_int(n - 1, lambda k: nth_new_moon(k) < tee))


# see lines 3587-3594 in calendrica-3.0.cl
def new_moon_at_or_after(tee):
    """Return the moment UT of first new moon at or after moment, tee."""
    t0 = nth_new_moon(0)
    phi = lunar_phase(tee)
    n = iround((tee - t0) / MEAN_SYNODIC_MONTH - phi / 360)
    return nth_new_moon(next_int(n, lambda k: nth_new_moon(k) >= tee))


# see lines 3596-3613 in calendrica-3.0.cl
def lunar_phase(tee):
    """Return the lunar phase, as an angle in degrees, at moment tee.
    An angle of 0 means a new moon, 90 degrees means the
    first quarter, 180 means a full moon, and 270 degrees
    means the last quarter."""
    phi = mod(lunar_longitude(tee) - solar_longitude(tee), 360)
    t0 = nth_new_moon(0)
    n = iround((tee - t0) / MEAN_SYNODIC_MONTH)
    phi_prime = (360 *
                 mod((tee - nth_new_moon(n)) / MEAN_SYNODIC_MONTH, 1))
    if abs(phi - phi_prime) > 180:
        return phi_prime
    else:
        return phi


# see lines 3615-3625 in calendrica-3.0.cl
def lunar_phase_at_or_before(phi, tee):
    """Return the moment UT of the last time at or before moment, tee,
    when the lunar_phase was phi degrees."""
    tau = (tee -
           (MEAN_SYNODIC_MONTH  *
            (1/360) *
            mod(lunar_phase(tee) - phi, 360)))
    a = tau - 2
    b = min(tee, tau +2)
    return invert_angular(lunar_phase, phi, a, b)


# see lines 3627-3631 in calendrica-3.0.cl
NEW = 0

# see lines 3633-3637 in calendrica-3.0.cl
FIRST_QUARTER = 90

# see lines 3639-3643 in calendrica-3.0.cl
FULL = 180

# see lines 3645-3649 in calendrica-3.0.cl
LAST_QUARTER = 270

# see lines 3651-3661 in calendrica-3.0.cl
def lunar_phase_at_or_after(phi, tee):
    """Return the moment UT of the next time at or after moment, tee,
    when the lunar_phase is phi degrees."""
    tau = (tee +
           (MEAN_SYNODIC_MONTH    *
            (1/360) *
            mod(phi - lunar_phase(tee), 360)))
    a = max(tee, tau - 2)
    b = tau + 2
    return invert_angular(lunar_phase, phi, a, b)




# see lines 3734-3762 in calendrica-3.0.cl
def lunar_altitude(tee, location):
    """Return the geocentric altitude of moon at moment, tee,
    at location, location, as a small positive/negative angle in degrees,
    ignoring parallax and refraction.  Adapted from 'Astronomical
    Algorithms' by Jean Meeus, Willmann_Bell, Inc., 1998."""
    phi = location.latitude
    psi = location.longitude
    lamb = lunar_longitude(tee)
    beta = lunar_latitude(tee)
    alpha = right_ascension(tee, beta, lamb)
    delta = declination(tee, beta, lamb)
    theta0 = sidereal_from_moment(tee)
    cap_H = mod(theta0 + psi - alpha, 360)
    altitude = arcsin_degrees(
        (sin_degrees(phi) * sin_degrees(delta)) +
        (cos_degrees(phi) * cos_degrees(delta) * cos_degrees(cap_H)))
    return mod(altitude + 180, 360) - 180
 

# see lines 3764-3813 in calendrica-3.0.cl
def lunar_distance(tee):
    """Return the distance to moon (in meters) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed."""
    c = julian_centuries(tee)
    cap_D = lunar_elongation(c)
    cap_M = solar_anomaly(c)
    cap_M_prime = lunar_anomaly(c)
    cap_F = moon_node(c)
    cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
    args_lunar_elongation = \
        [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1,
         1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2,
         2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2, 2,]
    args_solar_anomaly = \
        [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
         0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1,
         -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0, 0]
    args_lunar_anomaly = \
        [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2,
         -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0,
         -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3,
         2, 1, -1, 3, -1]
    args_moon_node = \
        [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0,
         0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, -2]
    cosine_coefficients = \
        [-20905355, -3699111, -2955968, -569925, 48888, -3149,
         246158, -152138, -170733, -204586, -129620, 108743,
         104755, 10321, 0, 79661, -34782, -23210, -21636, 24208,
         30824, -8379, -16675, -12831, -10445, -11650, 14403,
         -7003, 0, 10056, 6322, -9884, 5751, 0, -4950, 4130, 0,
         -3958, 0, 3258, 2616, -1897, -2117, 2354, 0, 0, -1423,
         -1117, -1571, -1739, 0, -4421, 0, 0, 0, 0, 1165, 0, 0,
         8752]
    correction = sigma ([cosine_coefficients,
                         args_lunar_elongation,
                         args_solar_anomaly,
                         args_lunar_anomaly,
                         args_moon_node],
                        lambda v, w, x, y, z: (v *
                                    pow(cap_E, abs(x)) * 
                                    cos_degrees((w * cap_D) +
                                                   (x * cap_M) +
                                                   (y * cap_M_prime) +
                                                   (z * cap_F))))
    return 385000560 + correction


def lunar_position(tee):
    """Return the moon position (geocentric latitude and longitude [in degrees]
    and distance [in meters]) at moment, tee.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 2nd ed."""
    return (lunar_latitude(tee), lunar_longitude(tee), lunar_distance(tee))

# see lines 3815-3824 in calendrica-3.0.cl
def lunar_parallax(tee, location):
    """Return the parallax of moon at moment, tee, at location, location.
    Adapted from "Astronomical Algorithms" by Jean Meeus,
    Willmann_Bell, Inc., 1998."""
    geo = lunar_altitude(tee, location)
    Delta = lunar_distance(tee)
    alt = 6378140 / Delta
    arg = alt * cos_degrees(geo)
    return arcsin_degrees(arg)


# see lines 3826-3832 in calendrica-3.0.cl
def topocentric_lunar_altitude(tee, location):
    """Return the topocentric altitude of moon at moment, tee,
    at location, location, as a small positive/negative angle in degrees,
    ignoring refraction."""
    return lunar_altitude(tee, location) - lunar_parallax(tee, location)


# see lines 3834-3839 in calendrica-3.0.cl
def lunar_diameter(tee):
    """Return the geocentric apparent lunar diameter of the moon (in
    degrees) at moment, tee.  Adapted from 'Astronomical
    Algorithms' by Jean Meeus, Willmann_Bell, Inc., 2nd ed."""
    return (1792367000/9) / lunar_distance(tee)


###########################################
# astronomical lunar calendars algorithms #
###########################################
# see lines 5829-5845 in calendrica-3.0.cl
def visible_crescent(date, location):
    """Return S. K. Shaukat's criterion for likely
    visibility of crescent moon on eve of date 'date',
    at location 'location'."""
    tee = location.universal_from_standard(location.dusk(date - 1, mpf(4.5)))
    phase = lunar_phase(tee)
    altitude = lunar_altitude(tee, location)
    arc_of_light = arccos_degrees(cos_degrees(lunar_latitude(tee)) *
                                  cos_degrees(phase))
    return ((NEW < phase < FIRST_QUARTER) and
            (mpf(10.6) <= arc_of_light <= 90) and
            (altitude > mpf(4.1)))

# see lines 5847-5860 in calendrica-3.0.cl
def phasis_on_or_before(date, location):
    """Return the closest fixed date on or before date 'date', when crescent
    moon first became visible at location 'location'."""
    mean = date - ifloor(lunar_phase(date + 1) / 360 *
                         MEAN_SYNODIC_MONTH)
    tau = ((mean - 30)
           if (((date - mean) <= 3) and (not visible_crescent(date, location)))
           else (mean - 2))
    return  next_int(tau, lambda d: visible_crescent(d, location))


# see lines 5898-5901 in calendrica-3.0.cl
JERUSALEM = Location(mpf(31.8), mpf(35.2), 800, Clock.days_from_hours(2))

# see lines 5903-5918 in calendrica-3.0.cl
def astronomical_easter(g_year):
    """Return date of (proposed) astronomical Easter in Gregorian
    year, g_year."""
    jan1 = GregorianDate.new_year(g_year)
    equinox = solar_longitude_after(SPRING, jan1)
    paschal_moon = ifloor(JERUSALEM.apparent_from_local(JERUSALEM.local_from_universal(lunar_phase_at_or_after(FULL, equinox))))
    # Return the Sunday following the Paschal moon.
    return DayOfWeek(DayOfWeek.Sunday).after(paschal_moon)

# see lines 5920-5923 in calendrica-3.0.cl
JAFFA = Location(angle(32, 1, 60), angle(34, 45, 0), 0, Clock.days_from_hours(2))

# see lines 5925-5938 in calendrica-3.0.cl
def phasis_on_or_after(date, location):
    """Return closest fixed date on or after date, date, on the eve
    of which crescent moon first became visible at location, location."""
    mean = date - ifloor(lunar_phase(date + 1) / mpf(360) *
                        MEAN_SYNODIC_MONTH)
    tau = (date if (((date - mean) <= 3) and
                    (not visible_crescent(date - 1, location)))
           else (mean + 29))
    return next_int(tau, lambda d: visible_crescent(d, location))










#####################################
# modern hindu calendars algorithms #
#####################################
# see lines 4816-4820 in calendrica-3.0.cl
def hindu_lunar_date(year, month, leap_month, day, leap_day):
    """Return a lunar Hindu date data structure."""
    return [year, month, leap_month, day, leap_day]


# see lines 4822-4824 in calendrica-3.0.cl
def hindu_lunar_month(date):
    """Return 'month' element of a lunar Hindu date, date."""
    return date[1]


# see lines 4826-4828 in calendrica-3.0.cl
def hindu_lunar_leap_month(date):
    """Return 'leap_month' element of a lunar Hindu date, date."""
    return date[2]


# see lines 4830-4832 in calendrica-3.0.cl
def hindu_lunar_day(date):
    """Return 'day' element of a lunar Hindu date, date."""
    return date[3]

# see lines 4834-4836 in calendrica-3.0.cl
def hindu_lunar_leap_day(date):
    """Return 'leap_day' element of a lunar Hindu date, date."""
    return date[4]

# see lines 4838-4840 in calendrica-3.0.cl
def hindu_lunar_year(date):
    """Return 'year' element of a lunar Hindu date, date."""
    return date[0]

# see lines 4842-4850 in calendrica-3.0.cl
def hindu_sine_table(entry):
    """Return the value for entry in the Hindu sine table.
    Entry, entry, is an angle given as a multiplier of 225'."""
    exact = 3438 * sin_degrees(entry * angle(0, 225, 0))
    error = 0.215 * signum(exact) * signum(abs(exact) - 1716)
    return iround(exact + error) / 3438


# see lines 4852-4861 in calendrica-3.0.cl
def hindu_sine(theta):
    """Return the linear interpolation for angle, theta, in Hindu table."""
    entry    = theta / angle(0, 225, 0)
    fraction = mod(entry, 1)
    return ((fraction * hindu_sine_table(iceiling(entry))) +
            ((1 - fraction) * hindu_sine_table(ifloor(entry))))


# see lines 4863-4873 in calendrica-3.0.cl
def hindu_arcsin(amp):
    """Return the inverse of Hindu sine function of amp."""
    if (amp < 0):
        return -hindu_arcsin(-amp)
    else:
        pos = next_int(0, lambda k: amp <= hindu_sine_table(k))
        below = hindu_sine_table(pos - 1)
        return (angle(0, 225, 0) *
                (pos - 1 + ((amp - below) / (hindu_sine_table(pos) - below))))


# see lines 4875-4878 in calendrica-3.0.cl
HINDU_SIDEREAL_YEAR = 365 + 279457/1080000

# see lines 4880-4883 in calendrica-3.0.cl
HINDU_CREATION = OldHindu.EPOCH - 1955880000 * HINDU_SIDEREAL_YEAR

# see lines 4885-4889 in calendrica-3.0.cl
def hindu_mean_position(tee, period):
    """Return the position in degrees at moment, tee, in uniform circular
    orbit of period days."""
    return 360 * mod((tee - HINDU_CREATION) / period, 1)

# see lines 4891-4894 in calendrica-3.0.cl
HINDU_SIDEREAL_MONTH = 27 + 4644439/14438334

# see lines 4896-4899 in calendrica-3.0.cl
HINDU_SYNODIC_MONTH = 29 + 7087771/13358334

# see lines 4901-4904 in calendrica-3.0.cl
HINDU_ANOMALISTIC_YEAR = 1577917828000/(4320000000 - 387)

# see lines 4906-4909 in calendrica-3.0.cl
HINDU_ANOMALISTIC_MONTH = mpf(1577917828)/(57753336 - 488199)

# see lines 4911-4926 in calendrica-3.0.cl
def hindu_true_position(tee, period, size, anomalistic, change):
    """Return the longitudinal position at moment, tee.
    period is the period of mean motion in days.
    size is ratio of radii of epicycle and deferent.
    anomalistic is the period of retrograde revolution about epicycle.
    change is maximum decrease in epicycle size."""
    lam         = hindu_mean_position(tee, period)
    offset      = hindu_sine(hindu_mean_position(tee, anomalistic))
    contraction = abs(offset) * change * size
    equation    = hindu_arcsin(offset * (size - contraction))
    return mod(lam - equation, 360)


# see lines 4928-4932 in calendrica-3.0.cl
def hindu_solar_longitude(tee):
    """Return the solar longitude at moment, tee."""
    return hindu_true_position(tee,
                               HINDU_SIDEREAL_YEAR,
                               14/360,
                               HINDU_ANOMALISTIC_YEAR,
                               1/42)


# see lines 4934-4938 in calendrica-3.0.cl
def hindu_zodiac(tee):
    """Return the zodiacal sign of the sun, as integer in range 1..12,
    at moment tee."""
    return quotient(float(hindu_solar_longitude(tee)), 30) + 1


# see lines 4940-4944 in calendrica-3.0.cl
def hindu_lunar_longitude(tee):
    """Return the lunar longitude at moment, tee."""
    return hindu_true_position(tee,
                               HINDU_SIDEREAL_MONTH,
                               32/360,
                               HINDU_ANOMALISTIC_MONTH,
                               1/96)


# see lines 4946-4952 in calendrica-3.0.cl
def hindu_lunar_phase(tee):
    """Return the longitudinal distance between the sun and moon
    at moment, tee."""
    return mod(hindu_lunar_longitude(tee) - hindu_solar_longitude(tee), 360)


# see lines 4954-4958 in calendrica-3.0.cl
def hindu_lunar_day_from_moment(tee):
    """Return the phase of moon (tithi) at moment, tee, as an integer in
    the range 1..30."""
    return quotient(hindu_lunar_phase(tee), 12) + 1


# see lines 4960-4973 in calendrica-3.0.cl
def hindu_new_moon_before(tee):
    """Return the approximate moment of last new moon preceding moment, tee,
    close enough to determine zodiacal sign."""
    varepsilon = pow(2, -1000)
    tau = tee - ((1/360)   *
                 hindu_lunar_phase(tee) *
                 HINDU_SYNODIC_MONTH)
    return binary_search(tau - 1, min(tee, tau + 1),
                         lambda l, u: ((hindu_zodiac(l) == hindu_zodiac(u)) or
                                       ((u - l) < varepsilon)),
                         lambda x: hindu_lunar_phase(x) < 180)


# see lines 4975-4988 in calendrica-3.0.cl
def hindu_lunar_day_at_or_after(k, tee):
    """Return the time lunar_day (tithi) number, k, begins at or after
    moment, tee.  k can be fractional (for karanas)."""
    phase = (k - 1) * 12
    tau   = tee + ((1/360) *
                   mod(phase - hindu_lunar_phase(tee), 360) *
                   HINDU_SYNODIC_MONTH)
    a = max(tee, tau - 2)
    b = tau + 2
    return invert_angular(hindu_lunar_phase, phase, a, b)


# see lines 4990-4996 in calendrica-3.0.cl
def hindu_calendar_year(tee):
    """Return the solar year at given moment, tee."""
    return iround(((tee - OldHindu.EPOCH) / HINDU_SIDEREAL_YEAR) -
                 (hindu_solar_longitude(tee) / 360))


# see lines 4998-5001 in calendrica-3.0.cl
HINDU_SOLAR_ERA = 3179

# see lines 5003-5020 in calendrica-3.0.cl
def hindu_solar_from_fixed(date):
    """Return the Hindu (Orissa) solar date equivalent to fixed date, date."""
    critical = hindu_sunrise(date + 1)
    month    = hindu_zodiac(critical)
    year     = hindu_calendar_year(critical) - HINDU_SOLAR_ERA
    approx   = date - 3 - mod(ifloor(hindu_solar_longitude(critical)), 30)
    begin    = next_int(approx,
                    lambda i: (hindu_zodiac(hindu_sunrise(i + 1)) ==  month))
    day      = date - begin + 1
    return OldHinduSolarDate(year, month, day)


# see lines 5022-5039 in calendrica-3.0.cl
def fixed_from_hindu_solar(s_date):
    """Return the fixed date corresponding to Hindu solar date, s_date,
    (Saka era; Orissa rule.)"""
    month = standard_month(s_date)
    day   = standard_day(s_date)
    year  = standard_year(s_date)
    begin = ifloor((year + HINDU_SOLAR_ERA + ((month - 1)/12)) *
                  HINDU_SIDEREAL_YEAR + OldHindu.EPOCH)
    return (day - 1 +
            next_int(begin - 3,
                 lambda d: (hindu_zodiac(hindu_sunrise(d + 1)) == month)))


# see lines 5041-5044 in calendrica-3.0.cl
HINDU_LUNAR_ERA = 3044

# see lines 5046-5074 in calendrica-3.0.cl
def hindu_lunar_from_fixed(date):
    """Return the Hindu lunar date, new_moon scheme, 
    equivalent to fixed date, date."""
    critical = hindu_sunrise(date)
    day      = hindu_lunar_day_from_moment(critical)
    leap_day = (day == hindu_lunar_day_from_moment(hindu_sunrise(date - 1)))
    last_new_moon = hindu_new_moon_before(critical)
    next_new_moon = hindu_new_moon_before(ifloor(last_new_moon) + 35)
    solar_month   = hindu_zodiac(last_new_moon)
    leap_month    = (solar_month == hindu_zodiac(next_new_moon))
    month    = amod(solar_month + 1, 12)
    year     = (hindu_calendar_year((date + 180) if (month <= 2) else date) -
                HINDU_LUNAR_ERA)
    return hindu_lunar_date(year, month, leap_month, day, leap_day)


# see lines 5076-5123 in calendrica-3.0.cl
def fixed_from_hindu_lunar(l_date):
    """Return the Fixed date corresponding to Hindu lunar date, l_date."""
    year       = hindu_lunar_year(l_date)
    month      = hindu_lunar_month(l_date)
    leap_month = hindu_lunar_leap_month(l_date)
    day        = hindu_lunar_day(l_date)
    leap_day   = hindu_lunar_leap_day(l_date)
    approx = OldHindu.EPOCH + (HINDU_SIDEREAL_YEAR *
                            (year + HINDU_LUNAR_ERA + ((month - 1) / 12)))
    s = ifloor(approx - ((1/360) *
                        HINDU_SIDEREAL_YEAR *
                        mod(hindu_solar_longitude(approx) -
                            ((month - 1) * 30) +
                            180, 360) -
                        180))
    k = hindu_lunar_day_from_moment(s + Clock.days_from_hours(6))
    if (3 < k < 27):
        temp = k
    else:
        mid = hindu_lunar_from_fixed(s - 15)
        if ((hindu_lunar_month(mid) != month) or
            (hindu_lunar_leap_month(mid) and not leap_month)):
            temp = mod(k + 15, 30) - 15
        else:
            temp = mod(k - 15, 30) + 15
    est = s + day - temp
    tau = (est -
           mod(hindu_lunar_day_from_moment(est + Clock.days_from_hours(6)) - day + 15, 30) +
           15)
    date = next_int(tau - 1,
                lambda d: (hindu_lunar_day_from_moment(hindu_sunrise(d)) in
                           [day, amod(day + 1, 30)]))
    return (date + 1) if leap_day else date


# see lines 5125-5139 in calendrica-3.0.cl
def hindu_equation_of_time(date):
    """Return the time from true to mean midnight of date, date."""
    offset = hindu_sine(hindu_mean_position(date, HINDU_ANOMALISTIC_YEAR))
    equation_sun = (offset *
                    angle(57, 18, 0) *
                    (14/360 - (abs(offset) / 1080)))
    return ((hindu_daily_motion(date) / 360) *
            (equation_sun / 360) *
            HINDU_SIDEREAL_YEAR)


# see lines 5141-5155 in calendrica-3.0.cl
def hindu_ascensional_difference(date, location):
    """Return the difference between right and oblique ascension
    of sun on date, date, at loacel, location."""
    sin_delta = (1397/3438) * hindu_sine(hindu_tropical_longitude(date))
    phi = location.latitude
    diurnal_radius = hindu_sine(90 + hindu_arcsin(sin_delta))
    tan_phi = hindu_sine(phi) / hindu_sine(90 + phi)
    earth_sine = sin_delta * tan_phi
    return hindu_arcsin(-earth_sine / diurnal_radius)


# see lines 5157-5172 in calendrica-3.0.cl
def hindu_tropical_longitude(date):
    """Return the Hindu tropical longitude on fixed date, date.
    Assumes precession with maximum of 27 degrees
    and period of 7200 sidereal years (= 1577917828/600 days)."""
    days = ifloor(date - OldHindu.EPOCH)
    precession = (27 -
                  (abs(54 -
                       mod(27 +
                           (108 * 600/1577917828 * days),
                           108))))
    return mod(hindu_solar_longitude(date) - precession, 360)


# see lines 5174-5183 in calendrica-3.0.cl
def hindu_rising_sign(date):
    """Return the tabulated speed of rising of current zodiacal sign on
    date, date."""
    i = quotient(float(hindu_tropical_longitude(date)), 30)
    return [1670/1800, 1795/1800, 1935/1800, 1935/1800,
            1795/1800, 1670/1800][mod(i, 6)]


# see lines 5185-5200 in calendrica-3.0.cl
def hindu_daily_motion(date):
    """Return the sidereal daily motion of sun on date, date."""
    mean_motion = 360 / HINDU_SIDEREAL_YEAR
    anomaly     = hindu_mean_position(date, HINDU_ANOMALISTIC_YEAR)
    epicycle    = 14/360 - abs(hindu_sine(anomaly)) / 1080
    entry       = quotient(float(anomaly), angle(0, 225, 0))
    sine_table_step = hindu_sine_table(entry + 1) - hindu_sine_table(entry)
    factor = -3438/225 * sine_table_step * epicycle
    return mean_motion * (factor + 1)

def hindu_solar_sidereal_difference(date):
    """Return the difference between solar and sidereal day on date, date."""
    return hindu_daily_motion(date) * hindu_rising_sign(date)

UJJAIN = Location(angle(23, 9, 0), angle(75, 46, 6), 0, Clock.days_from_hours(5 + 461/9000))

HINDU_LOCATION = UJJAIN

def hindu_sunrise(date):
    """Return the sunrise at hindu_location on date, date."""
    return (date + Clock.days_from_hours(6) + 
            ((UJJAIN.longitude - HINDU_LOCATION.longitude) / 360) -
            hindu_equation_of_time(date) +
            ((1577917828/1582237828 / 360) *
             (hindu_ascensional_difference(date, HINDU_LOCATION) +
              (1/4 * hindu_solar_sidereal_difference(date)))))


# see lines 5230-5244 in calendrica-3.0.cl
def hindu_fullmoon_from_fixed(date):
    """Return the Hindu lunar date, full_moon scheme, 
    equivalent to fixed date, date."""
    l_date     = hindu_lunar_from_fixed(date)
    year       = hindu_lunar_year(l_date)
    month      = hindu_lunar_month(l_date)
    leap_month = hindu_lunar_leap_month(l_date)
    day        = hindu_lunar_day(l_date)
    leap_day   = hindu_lunar_leap_day(l_date)
    m = (hindu_lunar_month(hindu_lunar_from_fixed(date + 20))
         if (day >= 16)
         else month)
    return hindu_lunar_date(year, m, leap_month, day, leap_day)


# see lines 5246-5255 in calendrica-3.0.cl
def is_hindu_expunged(l_month, l_year):
    """Return True if Hindu lunar month l_month in year, l_year
    is expunged."""
    return (l_month !=
            hindu_lunar_month(
                hindu_lunar_from_fixed(
                    fixed_from_hindu_lunar(
                        [l_year, l_month, False, 15, False]))))


# see lines 5257-5272 in calendrica-3.0.cl
def fixed_from_hindu_fullmoon(l_date):
    """Return the fixed date equivalent to Hindu lunar date, l_date,
    in full_moon scheme."""
    year       = hindu_lunar_year(l_date)
    month      = hindu_lunar_month(l_date)
    leap_month = hindu_lunar_leap_month(l_date)
    day        = hindu_lunar_day(l_date)
    leap_day   = hindu_lunar_leap_day(l_date)
    if (leap_month or (day <= 15)):
        m = month
    elif (is_hindu_expunged(amod(month - 1, 12), year)):
        m = amod(month - 2, 12)
    else:
        m = amod(month - 1, 12)
    return fixed_from_hindu_lunar(
        hindu_lunar_date(year, m, leap_month, day, leap_day))


# see lines 5274-5280 in calendrica-3.0.cl
def alt_hindu_sunrise(date):
    """Return the astronomical sunrise at Hindu location on date, date,
    per Lahiri, rounded to nearest minute, as a rational number."""
    rise = HINDU_LOCATION.dawn(date, angle(0, 47, 0))
    return 1/24 * 1/60 * iround(rise * 24 * 60)


# see lines 5282-5292 in calendrica-3.0.cl
def hindu_sunset(date):
    """Return sunset at HINDU_LOCATION on date, date."""
    return (date + Clock.days_from_hours(18) + 
            ((UJJAIN.longitude - HINDU_LOCATION.longitude) / 360) -
            hindu_equation_of_time(date) +
            (((1577917828/1582237828) / 360) *
             (- hindu_ascensional_difference(date, HINDU_LOCATION) +
              (3/4 * hindu_solar_sidereal_difference(date)))))


# see lines 5294-5313 in calendrica-3.0.cl
def hindu_sundial_time(tee):
    """Return Hindu local time of temporal moment, tee."""
    date = Clock.fixed_from_moment(tee)
    time = mod(tee, 1)
    q    = ifloor(4 * time)
    if (q == 0):
        a = hindu_sunset(date - 1)
        b = hindu_sunrise(date)
        t = Clock.days_from_hours(-6)
    elif (q == 3):
        a = hindu_sunset(date)
        b = hindu_sunrise(date + 1)
        t = Clock.days_from_hours(18)
    else:
        a = hindu_sunrise(date)
        b = hindu_sunset(date)
        t = Clock.days_from_hours(6)
    return a + (2 * (b - a) * (time - t))


# see lines 5315-5318 in calendrica-3.0.cl
def ayanamsha(tee):
    """Return the difference between tropical and sidereal solar longitude."""
    return solar_longitude(tee) - sidereal_solar_longitude(tee)


# see lines 5320-5323 in calendrica-3.0.cl
def astro_hindu_sunset(date):
    """Return the geometrical sunset at Hindu location on date, date."""
    return HINDU_LOCATION.dusk(date, 0)


# see lines 5325-5329 in calendrica-3.0.cl
def sidereal_zodiac(tee):
    """Return the sidereal zodiacal sign of the sun, as integer in range
    1..12, at moment, tee."""
    return quotient(int(sidereal_solar_longitude(tee)), 30) + 1


# see lines 5331-5337 in calendrica-3.0.cl
def astro_hindu_calendar_year(tee):
    """Return the astronomical Hindu solar year KY at given moment, tee."""
    return iround(((tee - OldHindu.EPOCH) / MEAN_SIDEREAL_YEAR) -
                 (sidereal_solar_longitude(tee) / 360))


# see lines 5339-5357 in calendrica-3.0.cl
def astro_hindu_solar_from_fixed(date):
    """Return the Astronomical Hindu (Tamil) solar date equivalent to
    fixed date, date."""
    critical = astro_hindu_sunset(date)
    month    = sidereal_zodiac(critical)
    year     = astro_hindu_calendar_year(critical) - HINDU_SOLAR_ERA
    approx   = (date - 3 -
                mod(ifloor(sidereal_solar_longitude( critical)), 30))
    begin    = next_int(approx,
                    lambda i: (sidereal_zodiac(astro_hindu_sunset(i)) == month))
    day      = date - begin + 1
    return OldHinduSolarDate(year, month, day)


# see lines 5359-5375 in calendrica-3.0.cl
def fixed_from_astro_hindu_solar(s_date):
    """Return the fixed date corresponding to Astronomical 
    Hindu solar date (Tamil rule; Saka era)."""
    month = standard_month(s_date)
    day   = standard_day(s_date)
    year  = standard_year(s_date)
    approx = (OldHindu.EPOCH - 3 +
              ifloor(((year + HINDU_SOLAR_ERA) + ((month - 1) / 12)) *
                    MEAN_SIDEREAL_YEAR))
    begin = next_int(approx,
                 lambda i: (sidereal_zodiac(astro_hindu_sunset(i)) == month))
    return begin + day - 1


# see lines 5377-5381 in calendrica-3.0.cl
def astro_lunar_day_from_moment(tee):
    """Return the phase of moon (tithi) at moment, tee, as an integer in
    the range 1..30."""
    return quotient(lunar_phase(tee), 12) + 1


# see lines 5383-5410 in calendrica-3.0.cl
def astro_hindu_lunar_from_fixed(date):
    """Return the astronomical Hindu lunar date equivalent to
    fixed date, date."""
    critical = alt_hindu_sunrise(date)
    day      = astro_lunar_day_from_moment(critical)
    leap_day = (day == astro_lunar_day_from_moment(
        alt_hindu_sunrise(date - 1)))
    last_new_moon = new_moon_before(critical)
    next_new_moon = new_moon_at_or_after(critical)
    solar_month   = sidereal_zodiac(last_new_moon)
    leap_month    = solar_month == sidereal_zodiac(next_new_moon)
    month    = amod(solar_month + 1, 12)
    year     = astro_hindu_calendar_year((date + 180)
                                         if (month <= 2)
                                         else date) - HINDU_LUNAR_ERA
    return hindu_lunar_date(year, month, leap_month, day, leap_day)


# see lines 5412-5460 in calendrica-3.0.cl
def fixed_from_astro_hindu_lunar(l_date):
    """Return the fixed date corresponding to Hindu lunar date, l_date."""
    year  = hindu_lunar_year(l_date)
    month = hindu_lunar_month(l_date)
    leap_month = hindu_lunar_leap_month(l_date)
    day   = hindu_lunar_day(l_date)
    leap_day = hindu_lunar_leap_day(l_date)
    approx = (OldHindu.EPOCH +
              MEAN_SIDEREAL_YEAR *
              (year + HINDU_LUNAR_ERA + ((month - 1) / 12)))
    s = ifloor(approx -
              1/360 * MEAN_SIDEREAL_YEAR *
              (mod(sidereal_solar_longitude(approx) -
                  (month - 1) * 30 + 180, 360) - 180))
    k = astro_lunar_day_from_moment(s + Clock.days_from_hours(6))
    if (3 < k < 27):
        temp = k
    else:
        mid = astro_hindu_lunar_from_fixed(s - 15)
        if ((hindu_lunar_month(mid) != month) or
            (hindu_lunar_leap_month(mid) and not leap_month)):
            temp = mod(k + 15, 30) - 15
        else:
            temp = mod(k - 15, 30) + 15
    est = s + day - temp
    tau = (est -
           mod(astro_lunar_day_from_moment(est + Clock.days_from_hours(6)) - day + 15, 30) +
           15)
    date = next_int(tau - 1,
                lambda d: (astro_lunar_day_from_moment(alt_hindu_sunrise(d)) in
                           [day, amod(day + 1, 30)]))
    return (date + 1) if leap_day else date


# see lines 5462-5467 in calendrica-3.0.cl
def hindu_lunar_station(date):
    """Return the Hindu lunar station (nakshatra) at sunrise on date, date."""
    critical = hindu_sunrise(date)
    return quotient(hindu_lunar_longitude(critical), angle(0, 800, 0)) + 1


# see lines 5469-5480 in calendrica-3.0.cl
def hindu_solar_longitude_at_or_after(lam, tee):
    """Return the moment of the first time at or after moment, tee
    when Hindu solar longitude will be lam degrees."""
    tau = tee + (HINDU_SIDEREAL_YEAR *
                 (1 / 360) *
                 mod(lam - hindu_solar_longitude(tee), 360))
    a = max(tee, tau - 5)
    b = tau +5
    return invert_angular(hindu_solar_longitude, lam, a, b)


# see lines 5482-5487 in calendrica-3.0.cl
def mesha_samkranti(g_year):
    """Return the fixed moment of Mesha samkranti (Vernal equinox)
    in Gregorian year, g_year."""
    jan1 = GregorianDate.new_year(g_year)
    return hindu_solar_longitude_at_or_after(0, jan1)


# see lines 5489-5493 in calendrica-3.0.cl
SIDEREAL_START = precession(HINDU_LOCATION.universal_from_local(mesha_samkranti(JulianDate.ce(285))))

# see lines 5495-5513 in calendrica-3.0.cl
def hindu_lunar_new_year(g_year):
    """Return the fixed date of Hindu lunisolar new year in
    Gregorian year, g_year."""
    jan1     = GregorianDate.new_year(g_year)
    mina     = hindu_solar_longitude_at_or_after(330, jan1)
    new_moon = hindu_lunar_day_at_or_after(1, mina)
    h_day    = ifloor(new_moon)
    critical = hindu_sunrise(h_day)
    return (h_day +
            (0 if ((new_moon < critical) or
                   (hindu_lunar_day_from_moment(hindu_sunrise(h_day + 1)) == 2))
             else 1))


# see lines 5515-5539 in calendrica-3.0.cl
def is_hindu_lunar_on_or_before(l_date1, l_date2):
    """Return True if Hindu lunar date, l_date1 is on or before
    Hindu lunar date, l_date2."""
    month1 = hindu_lunar_month(l_date1)
    month2 = hindu_lunar_month(l_date2)
    leap1  = hindu_lunar_leap_month(l_date1)
    leap2  = hindu_lunar_leap_month(l_date2)
    day1   = hindu_lunar_day(l_date1)
    day2   = hindu_lunar_day(l_date2)
    leap_day1 = hindu_lunar_leap_day(l_date1)
    leap_day2 = hindu_lunar_leap_day(l_date2)
    year1  = hindu_lunar_year(l_date1)
    year2  = hindu_lunar_year(l_date2)
    return ((year1 < year2) or
            ((year1 == year2) and
             ((month1 < month2) or
              ((month1 == month2) and
               ((leap1 and not leap2) or
                ((leap1 == leap2) and
                 ((day1 < day2) or
                  ((day1 == day2) and
                   ((not leap_day1) or
                    leap_day2)))))))))


# see lines 5941-5967 in calendrica-3.0.cl
def hindu_date_occur(l_month, l_day, l_year):
    """Return the fixed date of occurrence of Hindu lunar month, l_month,
    day, l_day, in Hindu lunar year, l_year, taking leap and
    expunged days into account.  When the month is
    expunged, then the following month is used."""
    lunar = hindu_lunar_date(l_year, l_month, False, l_day, False)
    ttry   = fixed_from_hindu_lunar(lunar)
    mid   = hindu_lunar_from_fixed((ttry - 5) if (l_day > 15) else ttry)
    expunged = l_month != hindu_lunar_month(mid)
    l_date = hindu_lunar_date(hindu_lunar_year(mid),
                              hindu_lunar_month(mid),
                              hindu_lunar_leap_month(mid),
                              l_day,
                              False)
    if (expunged):
        return next_int(ttry,
                    lambda d: (not is_hindu_lunar_on_or_before(
                        hindu_lunar_from_fixed(d),
                        l_date))) - 1
    elif (l_day != hindu_lunar_day(hindu_lunar_from_fixed(ttry))):
        return ttry - 1
    else:
        return ttry


# see lines 5969-5980 in calendrica-3.0.cl
def hindu_lunar_holiday(l_month, l_day, g_year):
    """Return the list of fixed dates of occurrences of Hindu lunar
    month, month, day, day, in Gregorian year, g_year."""
    l_year = hindu_lunar_year(
        hindu_lunar_from_fixed(GregorianDate.new_year(g_year)))
    date1  = hindu_date_occur(l_month, l_day, l_year)
    date2  = hindu_date_occur(l_month, l_day, l_year + 1)
    return list_range([date1, date2], GregorianDate.year_range(g_year))


# see lines 5582-5586 in calendrica-3.0.cl
def diwali(g_year):
    """Return the list of fixed date(s) of Diwali in Gregorian year, g_year."""
    return hindu_lunar_holiday(8, 1, g_year)


# see lines 5588-5605 in calendrica-3.0.cl
def hindu_tithi_occur(l_month, tithi, tee, l_year):
    """Return the fixed date of occurrence of Hindu lunar tithi prior
    to sundial time, tee, in Hindu lunar month, l_month, and
    year, l_year."""
    approx = hindu_date_occur(l_month, ifloor(tithi), l_year)
    lunar  = hindu_lunar_day_at_or_after(tithi, approx - 2)
    ttry    = Clock.fixed_from_moment(lunar)
    tee_h  = standard_from_sundial(ttry + tee, UJJAIN)
    if ((lunar <= tee_h) or
        (hindu_lunar_phase(standard_from_sundial(ttry + 1 + tee, UJJAIN)) >
         (12 * tithi))):
        return ttry
    else:
        return ttry + 1


# see lines 5607-5620 in calendrica-3.0.cl
def hindu_lunar_event(l_month, tithi, tee, g_year):
    """Return the list of fixed dates of occurrences of Hindu lunar tithi
    prior to sundial time, tee, in Hindu lunar month, l_month,
    in Gregorian year, g_year."""
    l_year = hindu_lunar_year(
        hindu_lunar_from_fixed(GregorianDate.new_year(g_year)))
    date1  = hindu_tithi_occur(l_month, tithi, tee, l_year)
    date2  = hindu_tithi_occur(l_month, tithi, tee, l_year + 1)
    return list_range([date1, date2],
                      GregorianDate.year_range(g_year))


# see lines 5622-5626 in calendrica-3.0.cl
def shiva(g_year):
    """Return the list of fixed date(s) of Night of Shiva in Gregorian
    year, g_year."""
    return hindu_lunar_event(11, 29, Clock.days_from_hours(24), g_year)


# see lines 5628-5632 in calendrica-3.0.cl
def rama(g_year):
    """Return the list of fixed date(s) of Rama's Birthday in Gregorian
    year, g_year."""
    return hindu_lunar_event(1, 9, Clock.days_from_hours(12), g_year)


# see lines 5634-5640 in calendrica-3.0.cl
def karana(n):
    """Return the number (0-10) of the name of the n-th (1-60) Hindu
    karana."""
    if (n == 1):
        return 0
    elif (n > 57):
        return n - 50
    else:
        return amod(n - 1, 7)


# see lines 5642-5648 in calendrica-3.0.cl
def yoga(date):
    """Return the Hindu yoga on date, date."""
    return ifloor(mod((hindu_solar_longitude(date) +
                 hindu_lunar_longitude(date)) / angle(0, 800, 0), 27)) + 1


# see lines 5650-5655 in calendrica-3.0.cl
def sacred_wednesdays(g_year):
    """Return the list of Wednesdays in Gregorian year, g_year,
    that are day 8 of Hindu lunar months."""
    return sacred_wednesdays_in_range(GregorianDate.year_range(g_year))


# see lines 5657-5672 in calendrica-3.0.cl
def sacred_wednesdays_in_range(range):
    """Return the list of Wednesdays within range of dates
    that are day 8 of Hindu lunar months."""
    a      = range[0]
    b      = range[1]
    wed    = DayOfWeek(DayOfWeek.Wednesday).on_or_after(a)
    h_date = hindu_lunar_from_fixed(wed)
    ell  = [wed] if (hindu_lunar_day(h_date) == 8) else []
    if is_in_range(wed, range):
        ell[:0] = sacred_wednesdays_in_range([wed + 1, b])
        return ell
    else:
        return []



# That's all folks!


