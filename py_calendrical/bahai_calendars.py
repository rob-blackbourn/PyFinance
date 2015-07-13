from operator import mod
from mpmath import mpf
from time_arithmatic import Clock
from py_cal_cal import quotient, next_int, ifloor, iround
from astro import SPRING, estimate_prior_solar_longitude, solar_longitude, MEAN_TROPICAL_YEAR
from location import Location
from gregorian_calendars import GregorianDate, JulianMonth

class BahaiDate(object):

    EPOCH = GregorianDate(1844, JulianMonth.March, 21).to_fixed()
    AYYAM_I_HA = 0
    
    def __init(self, major, cycle, year, month, day):
        self.major = major
        self.cycle = cycle
        self.year = year
        self.month = month
        self.day = day
        
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
    def from_fixed(cls, date):
        """Return Bahai date [major, cycle, year, month, day] corresponding
        to fixed date, date."""
        g_year = GregorianDate.to_year(date)
        start  = GregorianDate.to_year(cls.EPOCH)
        years  = (g_year - start -
                  (1 if (date <= 
                      GregorianDate(g_year, JulianMonth.March, 20).to_fixed()) else 0))
        major  = 1 + quotient(years, 361)
        cycle  = 1 + quotient(mod(years, 361), 19)
        year   = 1 + mod(years, 19)
        days   = date - BahaiDate(major, cycle, year, 1, 1).to_fixed()

        # month
        if (date >= BahaiDate(major, cycle, year, 19, 1).to_fixed()):
            month = 19
        elif (date >= BahaiDate(major, cycle, year, cls.AYYAM_I_HA, 1).to_fixed()):
            month = cls.AYYAM_I_HA
        else:
            month = 1 + quotient(days, 19)
    
        day = date + 1 - BahaiDate(major, cycle, year, month, 1).to_fixed()
    
        return BahaiDate(major, cycle, year, month, day)

    @classmethod    
    def new_year(cls, g_year):
        """Return fixed date of Bahai New Year in Gregorian year, g_year."""
        return GregorianDate(g_year, JulianMonth.March, 21).to_fixed()
    
    HAIFA = Location(mpf(32.82), 35, 0, Clock.days_from_hours(2))

    @classmethod    
    def sunset_in_haifa(cls, date):
        """Return universal time of sunset of evening
        before fixed date, date in Haifa."""
        return cls.HAIFA.universal_from_standard(cls.HAIFA.sunset(date))

    @classmethod    
    def future_new_year_on_or_before(cls, date):
        """Return fixed date of Future Bahai New Year on or
        before fixed date, date."""
        approx = estimate_prior_solar_longitude(SPRING, cls.sunset_in_haifa(date))
        return next_int(ifloor(approx) - 1,
                    lambda day: (solar_longitude(cls.sunset_in_haifa(day)) <=
                                 (SPRING + 2)))

    def to_future_fixed(self):
        """Return fixed date of Bahai date, b_date."""
        years = (361 * (self.major - 1)) + (19 * (self.cycle - 1)) + self.year
        if (self.month == 19):
            return (self.future_new_year_on_or_before(
                self.EPOCH +
                ifloor(MEAN_TROPICAL_YEAR * (years + 1/2))) -
                    20 + self.day)
        elif (self.month == self.AYYAM_I_HA):
            return (self.future_new_year_on_or_before(
                self.EPOCH +
                ifloor(MEAN_TROPICAL_YEAR * (years - 1/2))) +
                    341 + self.day)
        else:
            return (self.future_new_year_on_or_before(
                self.EPOCH +
                ifloor(MEAN_TROPICAL_YEAR * (years - 1/2))) +
                    (19 * (self.month - 1)) + self.day - 1)
    
    @classmethod
    def from_future_fixed(cls, date):
        """Return Future Bahai date corresponding to fixed date, date."""
        new_year = cls.future_new_year_on_or_before(date)
        years    = iround((new_year - cls.EPOCH) / MEAN_TROPICAL_YEAR)
        major    = 1 + quotient(years, 361)
        cycle    = 1 + quotient(mod(years, 361), 19)
        year     = 1 + mod(years, 19)
        days     = date - new_year
    
        if (date >= BahaiDate(major, cycle, year, 19, 1)).to_future_fixed():
            month = 19
        elif(date >= BahaiDate(major, cycle, year, cls.AYYAM_I_HA, 1).to_future_fixed()):
            month = cls.AYYAM_I_HA
        else:
            month = 1 + quotient(days, 19)
    
        day  = date + 1 - BahaiDate(major, cycle, year, month, 1).to_future_fixed()
    
        return BahaiDate(major, cycle, year, month, day)
    
    @classmethod    
    def feast_of_ridvan(cls, g_year):
        """Return Fixed date of Feast of Ridvan in Gregorian year year, g_year."""
        years = g_year - GregorianDate.to_year(cls.EPOCH)
        major = 1 + quotient(years, 361)
        cycle = 1 + quotient(mod(years, 361), 19)
        year = 1 + mod(years, 19)
        return BahaiDate(major, cycle, year, 2, 13).to_future_fixed()
