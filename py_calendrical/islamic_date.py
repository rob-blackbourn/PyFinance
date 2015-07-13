from py_calendrical.julian_date import JulianDate
from py_calendrical.gregorian_date import JulianMonth, GregorianDate
from core import mod, quotient
from fixed_date import list_range

class IslamicDate(object):

    EPOCH = JulianDate(JulianDate.ce(622), JulianMonth.July, 16).to_fixed()

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod    
    def is_leap_year(cls, year):
        """Return True if year is an Islamic leap year."""
        return mod(14 + 11 * year, 30) < 11
    
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
