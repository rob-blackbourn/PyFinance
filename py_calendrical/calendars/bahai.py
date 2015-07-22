from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.time_arithmatic import Clock
from py_calendrical.py_cal_cal import quotient, ifloor, iround
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.utils import reduce_cond, next_int
from py_calendrical.solar import Solar
from py_calendrical.astro import Astro

class BahaiDate(object):

    EPOCH = GregorianDate(1844, JulianMonth.March, 21).to_fixed()
    HAIFA = Location(mpf(32.82), 35, 0, Clock.days_from_hours(2))
    AYYAM_I_HA = 0
    
    def __init__(self, major, cycle, year, month, day):
        self.major = major
        self.cycle = cycle
        self.year = year
        self.month = month
        self.day = day
    
    def to_tuple(self):
        return (self.major, self.cycle, self.year, self.month, self.day)
    
    def to_fixed(self):
        raise NotImplementedError()

    @classmethod
    def from_fixed(cls, fixed_date):
        raise NotImplementedError()

    @classmethod    
    def new_year(cls, gregorian_year):
        """Return fixed date of Bahai New Year in Gregorian year, 'gregorian_year'."""
        return GregorianDate(gregorian_year, JulianMonth.March, 21).to_fixed()
    

    @classmethod    
    def sunset_in_haifa(cls, fixed_date):
        """Return universal time of sunset of evening
        before fixed date, 'fixed_date' in Haifa."""
        return cls.HAIFA.universal_from_standard(cls.HAIFA.sunset(fixed_date))

    def __eq__(self, other):
        return isinstance(other, BahaiDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, BahaiDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, BahaiDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, BahaiDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, BahaiDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)

class WesternBahaiDate(BahaiDate):
    
    def __init__(self, major, cycle, year, month, day):
        BahaiDate.__init__(self, major, cycle, year, month, day)
    
    def to_fixed(self):
        """Return fixed date equivalent to the Bahai date, b_date."""
        g_year = (361 * (self.major - 1) +
                  19 * (self.cycle - 1)  +
                  self.year - 1 +
                  GregorianDate.to_year(self.EPOCH))
        if (self.month == self.AYYAM_I_HA):
            elapsed_months = 342
        elif (self.month == 19):
            if (GregorianDate.is_leap_year(g_year + 1)):
                elapsed_months = 347
            else:
                elapsed_months = 346
        else:
            elapsed_months = 19 * (self.month - 1)
    
        return GregorianDate(g_year, JulianMonth.March, 20).to_fixed() + elapsed_months + self.day

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return Bahai date [major, cycle, year, month, day] corresponding
        to fixed date, 'fixed_date'."""
        g_year = GregorianDate.to_year(fixed_date)
        start  = GregorianDate.to_year(cls.EPOCH)
        years  = (g_year - start -
                  (1 if (fixed_date <= 
                      GregorianDate(g_year, JulianMonth.March, 20).to_fixed()) else 0))
        major  = 1 + quotient(years, 361)
        cycle  = 1 + quotient(mod(years, 361), 19)
        year   = 1 + mod(years, 19)
        days   = fixed_date - WesternBahaiDate(major, cycle, year, 1, 1).to_fixed()

        # month
        if fixed_date >= WesternBahaiDate(major, cycle, year, 19, 1).to_fixed():
            month = 19
        elif fixed_date >= WesternBahaiDate(major, cycle, year, cls.AYYAM_I_HA, 1).to_fixed():
            month = cls.AYYAM_I_HA
        else:
            month = 1 + quotient(days, 19)
    
        day = fixed_date + 1 - WesternBahaiDate(major, cycle, year, month, 1).to_fixed()
    
        return WesternBahaiDate(major, cycle, year, month, day)

class FutureBahaiDate(BahaiDate):
    
    def __init(self, major, cycle, year, month, day):
        BahaiDate.__init(self, major, cycle, year, month, day)
    
    def to_fixed(self):
        """Return fixed date of Bahai date, b_date."""
        years = (361 * (self.major - 1)) + (19 * (self.cycle - 1)) + self.year
        if self.month == 19:
            return self.new_year_on_or_before(self.EPOCH + ifloor(Solar.MEAN_TROPICAL_YEAR * (years + 1/2))) - 20 + self.day
        elif self.month == self.AYYAM_I_HA:
            return self.new_year_on_or_before(self.EPOCH + ifloor(Solar.MEAN_TROPICAL_YEAR * (years - 1/2))) + 341 + self.day
        else:
            return self.new_year_on_or_before(self.EPOCH + ifloor(Solar.MEAN_TROPICAL_YEAR * (years - 1/2))) + (19 * (self.month - 1)) + self.day - 1
    
    @classmethod
    def from_fixed(cls, fixed_date):
        """Return Future Bahai date corresponding to fixed date, 'fixed_date'."""
        new_year = cls.new_year_on_or_before(fixed_date)
        years    = iround((new_year - cls.EPOCH) / Solar.MEAN_TROPICAL_YEAR)
        major    = 1 + quotient(years, 361)
        cycle    = 1 + quotient(mod(years, 361), 19)
        year     = 1 + mod(years, 19)
        days     = fixed_date - new_year
    
        if fixed_date >= FutureBahaiDate(major, cycle, year, 19, 1).to_fixed():
            month = 19
        elif fixed_date >= FutureBahaiDate(major, cycle, year, cls.AYYAM_I_HA, 1).to_fixed():
            month = cls.AYYAM_I_HA
        else:
            month = 1 + quotient(days, 19)
    
        day = fixed_date + 1 - FutureBahaiDate(major, cycle, year, month, 1).to_fixed()
    
        return FutureBahaiDate(major, cycle, year, month, day)

    @classmethod    
    def new_year_on_or_before(cls, fixed_date):
        """Return fixed date of Future Bahai New Year on or
        before fixed date, 'fixed_date'."""
        approx = Solar.estimate_prior_solar_longitude(Astro.SPRING, cls.sunset_in_haifa(fixed_date))
        return next_int(ifloor(approx) - 1, lambda day: Solar.solar_longitude(cls.sunset_in_haifa(day)) <= Astro.SPRING + 2)

    @classmethod    
    def feast_of_ridvan(cls, gregorian_year):
        """Return Fixed date of Feast of Ridvan in Gregorian year year, 'gregorian_year'."""
        years = gregorian_year - GregorianDate.to_year(cls.EPOCH)
        major = 1 + quotient(years, 361)
        cycle = 1 + quotient(mod(years, 361), 19)
        year = 1 + mod(years, 19)
        return FutureBahaiDate(major, cycle, year, 2, 13).to_fixed()
