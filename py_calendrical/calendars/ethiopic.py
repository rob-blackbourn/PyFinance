from __future__ import division
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.coptic import CopticDate
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.month_of_year import MonthOfYear

class EthiopicDate(YearMonthDay):
    
    EPOCH = JulianDate(JulianDate.ce(8), MonthOfYear.August, 29).to_fixed()

    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)

    def to_fixed(self):
        """Return the fixed date corresponding to Ethiopic date 'e_date'."""
        return (self.EPOCH + CopticDate(self.year, self.month, self.day).to_fixed() - CopticDate.EPOCH)

    @classmethod
    def from_fixed(cls, date):
        """Return the Ethiopic date equivalent of fixed date 'date'."""
        ymd = CopticDate.from_fixed(date + (CopticDate.EPOCH - cls.EPOCH))
        return EthiopicDate(ymd.year, ymd.month, ymd.day)
