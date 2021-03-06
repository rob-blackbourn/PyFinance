from __future__ import division
from operator import mod
from py_calendrical.triganometry import angle
from py_calendrical.py_cal_cal import ifloor, iround, quotient
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate
from py_calendrical.time_arithmatic import Clock
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.utils import next_int
from py_calendrical.solar import Solar
from py_calendrical.astro import Astro
from py_calendrical.month_of_year import MonthOfYear

class FrenchDate(YearMonthDay):

    #"""Fixed date of start of the French Revolutionary calendar."""
    EPOCH = GregorianDate(1792, MonthOfYear.September, 22).to_fixed()
    PARIS = Location(angle(48, 50, 11), angle(2, 20, 15), 27, Clock.days_from_hours(1))
    
    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)

    def to_fixed(self):
        """Return fixed date of French Revolutionary date, f_date"""
        new_year = self.new_year_on_or_before(ifloor(self.EPOCH + 180 + Solar.MEAN_TROPICAL_YEAR * (self.year - 1)))
        return new_year - 1 + 30 * (self.month - 1) + self.day

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return French Revolutionary date of fixed date, 'fixed_date'."""
        new_year = cls.new_year_on_or_before(fixed_date)
        year  = iround((new_year - cls.EPOCH) / Solar.MEAN_TROPICAL_YEAR) + 1
        month = quotient(fixed_date - new_year, 30) + 1
        day   = mod(fixed_date - new_year, 30) + 1
        return FrenchDate(year, month, day)

    @classmethod        
    def midnight_in_paris(cls, date):
        """Return Universal Time of true midnight at the end of
           fixed date, date."""
        # tricky bug: I was using midDAY!!! So French Revolutionary was failing...
        return cls.PARIS.universal_from_standard(cls.PARIS.midnight(date + 1))

    @classmethod    
    def new_year_on_or_before(cls, date):
        """Return fixed date of French Revolutionary New Year on or
           before fixed date, date."""
        approx = Solar.estimate_prior_solar_longitude(Astro.AUTUMN, cls.midnight_in_paris(date))
        return next_int(ifloor(approx) - 1, lambda day: Astro.AUTUMN <= Solar.solar_longitude(cls.midnight_in_paris(day)))
    
    @classmethod
    def is_arithmetic_leap_year(cls, f_year):
        """Return True if year, f_year, is a leap year on the French
           Revolutionary calendar."""
        return ((mod(f_year, 4) == 0)                        and 
                (mod(f_year, 400) not in [100, 200, 300])  and
                (mod(f_year, 4000) != 0))
    
    def to_fixed_arithmetic(self):
        """Return fixed date of French Revolutionary date, f_date."""
        return (self.EPOCH - 1         +
                365 * (self.year - 1)         +
                quotient(self.year - 1, 4)    -
                quotient(self.year - 1, 100)  +
                quotient(self.year - 1, 400)  -
                quotient(self.year - 1, 4000) +
                30 * (self.month - 1)         +
                self.day)

    @classmethod    
    def from_fixed_arithmetic(cls, date):
        """Return French Revolutionary date [year, month, day] of fixed
           date, date."""
        approx = quotient(date - cls.EPOCH + 2, 1460969/4000) + 1
        year   = ((approx - 1)
                  if (date < FrenchDate(approx, 1, 1).to_fixed_arithmetic())
                  else approx)
        month  = 1 + quotient(date - FrenchDate(year, 1, 1).to_fixed_arithmetic(), 30)
        day    = date -  FrenchDate(year, month, 1).to_fixed_arithmetic() + 1
        return FrenchDate(year, month, day)
