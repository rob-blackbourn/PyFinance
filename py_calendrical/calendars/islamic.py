from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.py_cal_cal import quotient, ifloor, iround
from py_calendrical.time_arithmatic import Clock
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.year_month_day import YearMonthDay
from py_cal_cal.pycalcal import list_range
from py_calendrical.lunar import Lunar

class IslamicDate(YearMonthDay):

    EPOCH = JulianDate(JulianDate.ce(622), JulianMonth.July, 16).to_fixed()

    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)
    
    def to_fixed(self):
        raise NotImplementedError()

    @classmethod
    def from_fixed(cls, fixed_date):
        raise NotImplementedError()

    @classmethod    
    def is_leap_year(cls, year):
        """Return True if year is an Islamic leap year."""
        return mod(14 + 11 * year, 30) < 11

    @classmethod
    def in_gregorian(cls, month, day, gregorian_year):
        """Return list of the fixed dates of Islamic month 'month', day 'day' that
        occur in Gregorian year 'gregorian_year'."""
        jan1  = GregorianDate.new_year(gregorian_year)
        y     = cls.from_fixed(jan1).year
        date1 = IslamicDate(y, month, day).to_fixed()
        date2 = IslamicDate(y + 1, month, day).to_fixed()
        date3 = IslamicDate(y + 2, month, day).to_fixed()
        return list_range([date1, date2, date3], GregorianDate.year_range(gregorian_year))
    
    @classmethod
    def mawlid_an_nabi(cls, gregorian_year):
        """Return list of fixed dates of Mawlid_an_Nabi occurring in Gregorian
        year 'gregorian_year'."""
        return cls.in_gregorian(3, 12, gregorian_year)

class ArithmeticIslamicDate(IslamicDate):
    
    def __init__(self, year, month, day):
        IslamicDate.__init__(self, year, month, day)
    
    def to_fixed(self):
        """Return fixed date equivalent to this Islamic date."""
        return (self.EPOCH - 1 +
                (self.year - 1) * 354  +
                quotient(3 + 11 * self.year, 30) +
                29 * (self.month - 1) +
                quotient(self.month, 2) +
                self.day)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return Islamic date (year month day) corresponding to fixed date 'fixed_date'."""
        year       = quotient(30 * (fixed_date - cls.EPOCH) + 10646, 10631)
        prior_days = fixed_date - ArithmeticIslamicDate(year, 1, 1).to_fixed()
        month      = quotient(11 * prior_days + 330, 325)
        day        = fixed_date - ArithmeticIslamicDate(year, month, 1).to_fixed() + 1
        return ArithmeticIslamicDate(year, month, day)
        

class ObservationalIslamicDate(IslamicDate):
    
    # (Cairo, Egypt).
    LOCATION = Location(mpf(30.1), mpf(31.3), 200, Clock.days_from_hours(2))
    
    def __init__(self, year, month, day):
        IslamicDate.__init__(self, year, month, day)

    def to_fixed(self):
        """Return fixed date equivalent to Observational Islamic date, i_date."""
        midmonth = self.EPOCH + ifloor((((self.year - 1) * 12) + self.month - 0.5) * Lunar.MEAN_SYNODIC_MONTH)
        return (self.LOCATION.phasis_on_or_before(midmonth) + self.day - 1)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return Observational Islamic date (year month day)
        corresponding to fixed date, 'fixed_date'."""
        crescent = cls.LOCATION.phasis_on_or_before(fixed_date)
        elapsed_months = iround((crescent - cls.EPOCH) / Lunar.MEAN_SYNODIC_MONTH)
        year = quotient(elapsed_months, 12) + 1
        month = mod(elapsed_months, 12) + 1
        day = (fixed_date - crescent) + 1
        return ObservationalIslamicDate(year, month, day)
