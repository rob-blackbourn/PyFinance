from operator import mod
from mpmath import mpf
from py_calendrical.py_cal_cal import quotient, list_range, ifloor, iround
from py_calendrical.time_arithmatic import Clock
from py_calendrical.astro import phasis_on_or_before, MEAN_SYNODIC_MONTH
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.year_month_day import YearMonthDay

class IslamicDate(YearMonthDay):

    EPOCH = JulianDate(JulianDate.ce(622), JulianMonth.July, 16).to_fixed()

    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)
    
    def to_fixed(self):
        """Return fixed date equivalent to Islamic date i_date."""
        return (self.EPOCH - 1 +
                (self.year - 1) * 354  +
                quotient(3 + 11 * self.year, 30) +
                29 * (self.month - 1) +
                quotient(self.month, 2) +
                self.day)

    @classmethod
    def from_fixed(cls, date):
        """Return Islamic date (year month day) corresponding to fixed date date."""
        year       = quotient(30 * (date - cls.EPOCH) + 10646, 10631)
        prior_days = date - IslamicDate(year, 1, 1).to_fixed()
        month      = quotient(11 * prior_days + 330, 325)
        day        = date - IslamicDate(year, month, 1).to_fixed() + 1
        return IslamicDate(year, month, day)

    @classmethod    
    def is_leap_year(cls, year):
        """Return True if year is an Islamic leap year."""
        return mod(14 + 11 * year, 30) < 11

    @classmethod
    def in_gregorian(cls, i_month, i_day, g_year):
        """Return list of the fixed dates of Islamic month i_month, day i_day that
        occur in Gregorian year g_year."""
        jan1  = GregorianDate.new_year(g_year)
        y     = cls.from_fixed(jan1).year
        date1 = IslamicDate(y, i_month, i_day).to_fixed()
        date2 = IslamicDate(y + 1, i_month, i_day).to_fixed()
        date3 = IslamicDate(y + 2, i_month, i_day).to_fixed()
        return list_range([date1, date2, date3], GregorianDate.year_range(g_year))
    
    @classmethod
    def mawlid_an_nabi(cls, g_year):
        """Return list of fixed dates of Mawlid_an_Nabi occurring in Gregorian
        year g_year."""
        return cls.in_gregorian(3, 12, g_year)

# Sample location for Observational Islamic calendar
# (Cairo, Egypt).
ISLAMIC_LOCATION = Location(mpf(30.1), mpf(31.3), 200, Clock.days_from_hours(2))

def fixed_from_observational_islamic(i_date):
    """Return fixed date equivalent to Observational Islamic date, i_date."""
    midmonth = IslamicDate.EPOCH + ifloor((((i_date.year - 1) * 12) + i_date.month - 0.5) * MEAN_SYNODIC_MONTH)
    return (phasis_on_or_before(midmonth, ISLAMIC_LOCATION) + i_date.day - 1)

def observational_islamic_from_fixed(date):
    """Return Observational Islamic date (year month day)
    corresponding to fixed date, date."""
    crescent = phasis_on_or_before(date, ISLAMIC_LOCATION)
    elapsed_months = iround((crescent - IslamicDate.EPOCH) / MEAN_SYNODIC_MONTH)
    year = quotient(elapsed_months, 12) + 1
    month = mod(elapsed_months, 12) + 1
    day = (date - crescent) + 1
    return IslamicDate(year, month, day)
