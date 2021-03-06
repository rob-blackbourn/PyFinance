from __future__ import division
from operator import mod
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.py_cal_cal import quotient
from py_calendrical.calendars.julian import JulianDay

class EgyptianDate(YearMonthDay):

    EPOCH = JulianDay(1448638).to_fixed()    

    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)
        
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
