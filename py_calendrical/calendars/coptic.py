from __future__ import division
from operator import mod
from py_calendrical.py_cal_cal import quotient
from py_calendrical.calendars.gregorian import JulianMonth, GregorianDate
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.utils import list_range

class CopticDate(YearMonthDay):

    EPOCH = JulianDate(JulianDate.ce(284), JulianMonth.August, 29).to_fixed()
    
    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)

    @classmethod
    def is_leap_year(year):
        """Return True if Coptic year 'c_year' is a leap year
        in the Coptic calendar."""
        return mod(year, 4) == 3
    
    def to_fixed(self):
        """Return the fixed date of Coptic date."""
        return (self.EPOCH - 1  +
                365 * (self.year - 1)  +
                quotient(self.year, 4) +
                30 * (self.month - 1)  +
                self.day)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Coptic date equivalent of fixed date 'fixed_date'."""
        year  = quotient((4 * (fixed_date - cls.EPOCH)) + 1463, 1461)
        month = 1 + quotient(fixed_date - CopticDate(year, 1, 1).to_fixed(), 30)
        day   = fixed_date + 1 - CopticDate(year, month, 1).to_fixed()
        return CopticDate(year, month, day)

    @classmethod
    def in_gregorian(cls, c_month, c_day, g_year):
        """Return the list of the fixed dates of Coptic month 'c_month',
        day 'c_day' that occur in Gregorian year 'g_year'."""
        jan1  = GregorianDate.new_year(g_year)
        y     = cls.from_fixed(jan1).year
        date1 = CopticDate(y, c_month, c_day).to_fixed()
        date2 = CopticDate(y+1, c_month, c_day).to_fixed()
        return list_range([date1, date2], GregorianDate.year_range(g_year))

    @classmethod    
    def christmas(cls, g_year):
        """Retuen the list of zero or one fixed dates of Coptic Christmas
        dates in Gregorian year 'g_year'."""
        return cls.coptic_in_gregorian(4, 29, g_year)
