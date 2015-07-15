from operator import mod
from enum import IntEnum
import datetime
from py_calendrical.py_cal_cal import quotient, amod
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.year_month_day import YearMonthDay
from fractions import Fraction

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

class GregorianDate(YearMonthDay):    

    EPOCH = 1

    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)

    def to_fixed(self):
        """Return the serial date equivalent."""
        return ((self.EPOCH - 1) + 
                (365 * (self.year -1)) + 
                quotient(self.year - 1, 4) - 
                quotient(self.year - 1, 100) + 
                quotient(self.year - 1, 400) + 
                quotient((367 * self.month) - 362, 12) + 
                (0 if self.month <= 2 else (-1 if self.is_leap_year(self.year) else -2)) + self.day)

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

    def to_date(self):
        return datetime.date(self.year, self.month, self.day)
    
    @classmethod
    def from_date(cls, date):
        return GregorianDate(date.year, date.month, date.day)
    
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
        return year if n100 == 4 or n1 == 4 else year + 1

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
    def date_difference(cls, gregorian_date1, gregorian_date2):
        """Return the number of days from date 'date1'
        till date 'date2'."""
        return gregorian_date2.to_fixed() - gregorian_date1.to_fixed()
    
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
        approx = quotient(fixed_date - cls.EPOCH + 2, Fraction(146097, 400))
        start  = (cls.EPOCH        +
                  (365 * approx)         +
                  quotient(approx, 4)    +
                  -quotient(approx, 100) +
                  quotient(approx, 400))
        return approx if fixed_date < start else approx + 1

    def nth_day_of_week(self, n, day_of_week):
        """Return the fixed date of n-th day of week.
        If n>0, return the n-th day of week on or after this date.
        If n<0, return the n-th day of week on or before this date.
        If n=0, return raise an error.
        A k-day of 0 means Sunday, 1 means Monday, and so on."""
        if n > 0:
            return 7 * n + day_of_week.before(self.to_fixed())
        elif n < 0:
            return 7 * n + day_of_week.after(self.to_fixed())
        else:
            raise ValueError("No valid answer where 'n' == 0.")

    def first_day_of_week(self, day_of_week):
        """Return the fixed date of first day of week on or after this date."""
        return self.nth_day_of_week(1, day_of_week)
    
    def last_day_of_week(self, day_of_week):
        """Return the fixed date of last day of week on or before this date."""
        return self.nth_day_of_week(-1, day_of_week)

def alt_orthodox_easter(year):
    """Return fixed date of Orthodox Easter in Gregorian year g_year.
    Alternative calculation."""
    paschal_moon = (354 * year +
                    30 * quotient((7 * year) + 8, 19) +
                    quotient(year, 4)  -
                    quotient(year, 19) -
                    273 +
                    GregorianDate.EPOCH)
    return DayOfWeek.Sunday.after(paschal_moon)

def easter(year):
    """Return fixed date of Easter in Gregorian year g_year."""
    century = quotient(year, 100) + 1
    shifted_epact = mod(14 +
                        11 * mod(year, 19) -
                        quotient(3 * century, 4) +
                        quotient(5 + (8 * century), 25), 30)
    adjusted_epact = shifted_epact + 1 if shifted_epact == 0 or (shifted_epact == 1 and 10 < mod(year, 19)) else shifted_epact
    paschal_moon = GregorianDate(year, JulianMonth.April, 19).to_fixed() - adjusted_epact
    return DayOfWeek.Sunday.after(paschal_moon)

def pentecost(year):
    """Return fixed date of Pentecost in Gregorian year g_year."""
    return easter(year) + 49

def labor_day(year):
    """Return the fixed date of United States Labor Day in Gregorian
    year 'g_year' (the first Monday in September)."""
    return GregorianDate(year, JulianMonth.September, 1).first_day_of_week(DayOfWeek.Monday)

def memorial_day(year):
    """Return the fixed date of United States' Memorial Day in Gregorian
    year 'year' (the last Monday in May)."""
    return GregorianDate(year, JulianMonth.May, 31).last_day_of_week(DayOfWeek.Monday)

def election_day(year):
    """Return the fixed date of United States' Election Day in Gregorian
    year 'year' (the Tuesday after the first Monday in November)."""
    return GregorianDate(year, JulianMonth.November, 2).first_day_of_week(DayOfWeek.Tuesday)

def daylight_saving_start(year):
    """Return the fixed date of the start of United States daylight
    saving time in Gregorian year 'year' (the second Sunday in March)."""
    return GregorianDate(year, JulianMonth.March, 1).nth_day_of_week(2, DayOfWeek.Sunday)

def daylight_saving_end(year):
    """Return the fixed date of the end of United States daylight saving
    time in Gregorian year 'year' (the first Sunday in November)."""
    return GregorianDate(year, JulianMonth.November, 1).first_day_of_week(DayOfWeek.Sunday)

def christmas(year):
    """Return the fixed date of Christmas in Gregorian year 'year'."""
    return GregorianDate(year, JulianMonth.December, 25).to_fixed()

@classmethod    
def advent(year):
    """Return the fixed date of Advent in Gregorian year 'year'
    (the Sunday closest to November 30)."""
    return DayOfWeek.Sunday.nearest(GregorianDate(year, JulianMonth.November, 30).to_fixed())

def epiphany(year):
    """Return the fixed date of Epiphany in U.S. in Gregorian year 'year'
    (the first Sunday after January 1)."""
    return GregorianDate(year, JulianMonth.January, 2).first_day_of_week(DayOfWeek.Sunday)

def epiphany_it(year):
    """Return fixed date of Epiphany in Italy in Gregorian year 'year'."""
    return GregorianDate(year, JulianMonth.January, 6)

def unlucky_fridays_in_range(first_fixed_date, last_fixed_date):
    """Return the list of Fridays within range 'range' of fixed dates that
    are day 13 of the relevant Gregorian months."""
    fri  = DayOfWeek.Friday.on_or_after(first_fixed_date)
    date = GregorianDate.from_fixed(fri)
    ell  = [fri] if (date.day == 13) else []
    
    if first_fixed_date <= fri <= last_fixed_date:
        ell[:0] = unlucky_fridays_in_range(fri + 1, last_fixed_date)
        return ell
    else:
        return []
