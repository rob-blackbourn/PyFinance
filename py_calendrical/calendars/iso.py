from __future__ import division
from py_calendrical.py_cal_cal import amod, quotient, rd
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.calendars.gregorian import GregorianDate
from py_calendrical.utils import reduce_cond
from py_calendrical.month_of_year import MonthOfYear

class IsoDate(object):
    
    def __init__(self, year, week, day):
        self.year = year
        self.week = week
        self.day = day
        
    def to_fixed(self):
        """Return the fixed date equivalent to ISO date 'i_date'."""
        return GregorianDate(self.year - 1, MonthOfYear.December, 28).nth_day_of_week(self.week, DayOfWeek.Sunday) + self.day
    
    @classmethod
    def from_fixed(cls, date):
        """Return the ISO date corresponding to the fixed date 'date'."""
        approx = GregorianDate.to_year(date - 3)
        year   = (approx +
                  1 if date >= IsoDate(approx + 1, 1, 1).to_fixed()
                  else approx)
        week   = 1 + quotient(date - IsoDate(year, 1, 1).to_fixed(), 7)
        day    = amod(date - rd(0), 7)
        return IsoDate(year, week, day)

    @classmethod    
    def is_long_year(cls, i_year):
        """Return True if ISO year 'i_year' is a long (53-week) year."""
        jan1  = DayOfWeek.from_fixed(GregorianDate.new_year(i_year))
        dec31 = DayOfWeek._from_fixed(GregorianDate.year_end(i_year))
        return jan1 == DayOfWeek.Thursday or dec31 == DayOfWeek.Thursday

    def to_tuple(self):
        return (self.year, self.week, self.day)
    
    def __eq__(self, other):
        return isinstance(other, IsoDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, IsoDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, IsoDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, IsoDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, IsoDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    

