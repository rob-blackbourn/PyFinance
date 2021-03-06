from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.py_cal_cal import quotient, ifloor
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.calendars.gregorian import GregorianDate
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.utils import list_range
from py_calendrical.month_of_year import MonthOfYear

class JulianDay(object):
    
    EPOCH = mpf(-1721424.5)

    def __init__(self, date_from_epoch):
        self.julian_day = date_from_epoch
    
    def to_fixed(self):
        return ifloor(self.to_moment())

    @classmethod
    def from_fixed(cls, fixed_date):
        return cls.from_moment(fixed_date)
    
    def to_moment(self):
        return self.julian_day + self.EPOCH

    @classmethod
    def from_moment(cls, tee):
        return JulianDay(tee - cls.EPOCH)

class ModifiedJulianDay(object):
    
    EPOCH = 678576

    def __init__(self, date_from_epoch):
        self.modified_julian_day = date_from_epoch

    def to_fixed(self):
        return self.modified_julian_day + self.EPOCH

    @classmethod
    def from_fixed(cls, fixed_date):
        return ModifiedJulianDay(fixed_date - cls.EPOCH)

class JulianDate(YearMonthDay):
    
    EPOCH = GregorianDate(0, MonthOfYear.December, 30).to_fixed()
    
    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)

    def to_fixed(self):
        """Return the fixed date equivalent to the Julian date 'j_date'."""
        y     = self.year + 1 if self.year < 0 else self.year
        return (self.EPOCH - 1 +
                (365 * (y - 1)) +
                quotient(y - 1, 4) +
                quotient(367*self.month - 362, 12) +
                (0 if self.month <= 2 else (-1 if self.is_leap_year(self.year) else -2)) +
                self.day)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Julian fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        approx     = quotient(((4 * (fixed_date - cls.EPOCH))) + 1464, 1461)
        year       = approx - 1 if approx <= 0 else approx
        prior_days = fixed_date - JulianDate(year, MonthOfYear.January, 1).to_fixed()
        correction = (0 if fixed_date < JulianDate(year, MonthOfYear.March, 1).to_fixed()
                      else (1 if cls.is_leap_year(year) else 2))
        month      = quotient(12*(prior_days + correction) + 373, 367)
        day        = 1 + (fixed_date - JulianDate(year, month, 1).to_fixed())
        return JulianDate(year, month, day)
        
    @classmethod
    def bce(cls, n):
        """Return a negative value to indicate a BCE Julian year."""
        return -n
    
    @classmethod
    def ce(cls, n):
        """Return a positive value to indicate a CE Julian year."""
        return n

    @classmethod
    def is_leap_year(cls, year):
        """Return True if Julian year 'year' is a leap year in
        the Julian calendar."""
        return mod(year, 4) == (0 if year > 0 else 3)

    @classmethod
    def julian_year_from_auc_year(cls, year):
        """Return the Julian year equivalent to AUC year 'year'."""
        return ((year + cls.YEAR_ROME_FOUNDED - 1) 
                if (1 <= year <= (year - cls.YEAR_ROME_FOUNDED))
                else (year + cls.YEAR_ROME_FOUNDED))
    
    @classmethod
    def auc_year_from_julian_year(cls, year):
        """Return the AUC year equivalent to Julian year 'year'."""
        return ((year - cls.YEAR_ROME_FOUNDED - 1)
                if (cls.YEAR_ROME_FOUNDED <= year <= -1)
                else (year - cls.YEAR_ROME_FOUNDED))
    
    
    @classmethod
    def julian_in_gregorian(j_month, j_day, g_year):
        """Return the list of the fixed dates of Julian month 'j_month', day
        'j_day' that occur in Gregorian year 'g_year'."""
        jan1 = GregorianDate.new_year(g_year)
        y    = JulianDate.from_fixed(jan1).year
        y_prime = 1 if (y == -1) else (y + 1)
        date1 = JulianDate(y, j_month, j_day).to_fixed()
        date2 = JulianDate(y_prime, j_month, j_day).to_fixed()
        return list_range([date1, date2], GregorianDate.year_range(g_year))

    @classmethod
    def eastern_orthodox_christmas(cls, g_year):
        """Return the list of zero or one fixed dates of Eastern Orthodox Christmas
        in Gregorian year 'g_year'."""
        return cls.julian_in_gregorian(MonthOfYear.December, 25, g_year)

#######################################
# ecclesiastical calendars algorithms #
#######################################
def orthodox_easter(g_year):
    """Return fixed date of Orthodox Easter in Gregorian year g_year."""
    shifted_epact = mod(14 + 11 * mod(g_year, 19), 30)
    j_year        = g_year if g_year > 0 else g_year - 1
    paschal_moon  = JulianDate(j_year, MonthOfYear.April, 19).to_fixed() - shifted_epact
    return DayOfWeek.Sunday.after(paschal_moon)

def alt_orthodox_easter(g_year):
    """Return fixed date of Orthodox Easter in Gregorian year g_year.
    Alternative calculation."""
    paschal_moon = (354 * g_year +
                    30 * quotient((7 * g_year) + 8, 19) +
                    quotient(g_year, 4)  -
                    quotient(g_year, 19) -
                    273 +
                    GregorianDate.EPOCH)
    return DayOfWeek.Sunday.after(paschal_moon)

# see lines 1429-1431 in calendrica-3.0.cl
def pentecost(g_year):
    """Return fixed date of Pentecost in Gregorian year g_year."""
    return easter(g_year) + 49

def eastern_orthodox_christmas(year):
    """Return the list of zero or one fixed dates of Eastern Orthodox Christmas
    in Gregorian year 'year'."""
    return JulianDate.julian_in_gregorian(MonthOfYear.December, 25, year)
