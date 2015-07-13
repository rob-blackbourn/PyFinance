from operator import mod
from mpmath import mpf
from py_cal_cal import next_int, ifloor, iceiling, iround, quotient
from py_cal_cal import GregorianDate, JulianMonth, Clock
from astro import estimate_prior_solar_longitude, SPRING, solar_longitude, MEAN_TROPICAL_YEAR
from julian_calendars import JulianDate
from location import Location

class PersianDate(object):

    EPOCH = JulianDate(JulianDate.ce(622), JulianMonth.March, 19).to_fixed()
    TEHRAN = Location(mpf(35.68), mpf(51.42), 1100, Clock.days_from_hours(3 + 1/2))
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod        
    def midday_in_tehran(cls, date):
        """Return  Universal time of midday on fixed date, date, in Tehran."""
        return cls.TEHRAN.universal_from_standard(cls.TEHRAN.midday(date))
    
    @classmethod        
    def new_year_on_or_before(cls, date):
        """Return the fixed date of Astronomical Persian New Year on or
        before fixed date, date."""
        approx = estimate_prior_solar_longitude(SPRING, cls.midday_in_tehran(date))
        return next_int(ifloor(approx) - 1, lambda day: (solar_longitude(cls.midday_in_tehran(day)) <= (SPRING + 2)))

    def to_fixed(self):
        """Return fixed date of Astronomical Persian date, p_date."""
        temp = (self.year - 1) if (0 < self.year) else self.year
        new_year = self.new_year_on_or_before(self.EPOCH + 180 + ifloor(MEAN_TROPICAL_YEAR * temp))
        return ((new_year - 1) +
                ((31 * (self.month - 1)) if (self.month <= 7) else (30 * (self.month - 1) + 6)) +
                self.day)

    @classmethod        
    def from_fixed(cls, date):
        """Return Astronomical Persian date (year month day)
        corresponding to fixed date, date."""
        new_year = cls.new_year_on_or_before(date)
        y = iround((new_year - cls.EPOCH) / MEAN_TROPICAL_YEAR) + 1
        year = y if (0 < y) else (y - 1)
        day_of_year = date - PersianDate(year, 1, 1).to_fixed() + 1
        month = (iceiling(day_of_year / 31)
                 if (day_of_year <= 186)
                 else iceiling((day_of_year - 6) / 30))
        day = date - (PersianDate(year, month, 1).to_fixed() - 1)
        return PersianDate(year, month, day)
    
    @classmethod
    def is_arithmetic_leap_year(cls, p_year):
        """Return True if p_year is a leap year on the Persian calendar."""
        y    = (p_year - 474) if (0 < p_year) else (p_year - 473)
        year =  mod(y, 2820) + 474
        return  mod((year + 38) * 31, 128) < 31

    # see lines 3934-3958 in calendrica-3.0.cl
    def to_fixed_arithmetic(self):
        """Return fixed date equivalent to Persian date p_date."""
        y      = (self.year - 474) if (0 < self.year) else (self.year - 473)
        year   = mod(y, 2820) + 474
        temp   = (31 * (self.month - 1)) if (self.month <= 7) else ((30 * (self.month - 1)) + 6)
    
        return ((self.EPOCH - 1) 
                + (1029983 * quotient(y, 2820))
                + (365 * (year - 1))
                + quotient((31 * year) - 5, 128)
                + temp
                + self.day)

    @classmethod
    def to_arithmetic_year(cls, date):
        """Return Persian year corresponding to the fixed date, date."""
        d0    = date - PersianDate(475, 1, 1).to_fixed_arithmetic()
        n2820 = quotient(d0, 1029983)
        d1    = mod(d0, 1029983)
        y2820 = 2820 if (d1 == 1029982) else (quotient((128 * d1) + 46878, 46751))
        year  = 474 + (2820 * n2820) + y2820
    
        return year if (0 < year) else (year - 1)

    @classmethod
    def from_arithmetic_fixed(cls, date):
        """Return the Persian date corresponding to fixed date, date."""
        year        = cls.to_arithmetic_year(date)
        day_of_year = 1 + date - PersianDate(year, 1, 1).to_fixed_arithmetic()
        month       = (iceiling(day_of_year / 31)
                       if (day_of_year <= 186)
                       else iceiling((day_of_year - 6) / 30))
        day = date - PersianDate(year, month, 1).to_fixed_arithmetic() +1
        return PersianDate(year, month, day)
    
    @classmethod
    def naw_ruz(cls, g_year):
        """Return the Fixed date of Persian New Year (Naw-Ruz) in Gregorian
           year g_year."""
        persian_year = g_year - GregorianDate.to_year(cls.EPOCH) + 1
        y = (persian_year - 1) if (persian_year <= 0) else persian_year
        return PersianDate(y, 1, 1).to_fixed()
