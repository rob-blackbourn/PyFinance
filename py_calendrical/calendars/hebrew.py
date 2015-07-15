from __future__ import division
from operator import mod
from fractions import Fraction
from enum import IntEnum
from mpmath import mpf
from py_calendrical.py_cal_cal import quotient, summa, iround, ifloor
from py_calendrical.triganometry import angle
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.coptic import CopticDate
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.time_arithmatic import Clock
from py_calendrical.year_month_day import YearMonthDay
from py_calendrical.utils import next_int, final_int, list_range
from py_calendrical.lunar import Lunar
from py_calendrical.astro import Astro
from py_calendrical.solar import Solar

class HebrewMonth(IntEnum):
    NISAN = 1
    IYYAR = 2
    SIVAN = 3
    TAMMUZ = 4
    AV = 5
    ELUL = 6
    TISHRI = 7
    MARHESHVAN = 8
    KISLEV = 9
    TEVET = 10
    SHEVAT = 11
    ADAR = 12
    ADARII = 13
    
class HebrewDate(YearMonthDay):

    EPOCH = JulianDate(JulianDate.bce(3761),  JulianMonth.October, 7).to_fixed()
    
    def __init__(self, year, month, day):
        YearMonthDay.__init__(self, year, month, day)
    
    def to_fixed(self):
        """Return fixed date of Hebrew date h_date."""
        if self.month < HebrewMonth.TISHRI:
            tmp = (summa(lambda m: self.last_day_of_month(m, self.year),
                         HebrewMonth.TISHRI,
                         lambda m: m <= self.last_month_of_year(self.year)) +
                   summa(lambda m: self.last_day_of_month(m, self.year),
                         HebrewMonth.NISAN,
                         lambda m: m < self.month))
        else:
            tmp = summa(lambda m: self.last_day_of_month(m, self.year),
                        HebrewMonth.TISHRI,
                        lambda m: m < self.month)
    
        return self.new_year(self.year) + self.day - 1 + tmp

    @classmethod    
    def from_fixed(cls, fixed_date):
        """Return  Hebrew (year month day) corresponding to fixed date 'fixed_date'.
        # The fraction can be approximated by 365.25."""
        approx = quotient(fixed_date - cls.EPOCH, Fraction(35975351, 98496)) + 1
        year = final_int(approx - 1, lambda y: cls.new_year(y) <= fixed_date)
        start = HebrewMonth.TISHRI if fixed_date < HebrewDate(year, HebrewMonth.NISAN, 1).to_fixed() else  HebrewMonth.NISAN
        month = next_int(start, lambda m: fixed_date <= HebrewDate(year, m, cls.last_day_of_month(m, year)).to_fixed())
        day = fixed_date - HebrewDate(year, month, 1).to_fixed() + 1
        return HebrewDate(year, month, day)

    @classmethod
    def is_leap_year(cls, year):
        """Return True if h_year is a leap year on Hebrew calendar."""
        return mod(7 * year + 1, 19) < 7

    @classmethod    
    def last_month_of_year(cls, year):
        """Return last month of Hebrew year."""
        return HebrewMonth.ADARII if cls.is_leap_year(year) else HebrewMonth.ADAR

    @classmethod    
    def is_sabbatical_year(cls, year):
        """Return True if year is a sabbatical year on the Hebrew calendar."""
        return mod(year, 7) == 0

    @classmethod    
    def last_day_of_month(cls, month, year):
        """Return last day of month month in Hebrew year year."""
        if (month in [HebrewMonth.IYYAR, HebrewMonth.TAMMUZ, HebrewMonth.ELUL, HebrewMonth.TEVET, HebrewMonth.ADARII]
            or (month == HebrewMonth.ADAR and not cls.is_leap_year(year))
            or (month == HebrewMonth.MARHESHVAN and not cls.is_long_marheshvan(year))
            or (month == HebrewMonth.KISLEV and cls.is_short_kislev(year))):
            return 29
        else:
            return 30

    @classmethod    
    def molad(cls, month, year):
        """Return moment of mean conjunction of month in Hebrew year."""
        y = year + 1 if month < HebrewMonth.TISHRI else year
        months_elapsed = month - HebrewMonth.TISHRI + quotient(235 * y - 234, 19)
        return cls.EPOCH - Fraction(876, 25920) + months_elapsed * (29 + Clock.days_from_hours(12) + Fraction(793,25920))

    @classmethod    
    def elapsed_days(cls, year):
        """Return number of days elapsed from the (Sunday) noon prior
        to the epoch of the Hebrew calendar to the mean
        conjunction (molad) of Tishri of Hebrew year h_year,
        or one day later."""
        months_elapsed = quotient(235 * year - 234, 19)
        parts_elapsed  = 12084 + 13753 * months_elapsed
        days = 29 * months_elapsed + quotient(parts_elapsed, 25920)
        return days + 1 if mod(3 * (days + 1), 7) < 3 else days

    @classmethod    
    def new_year(cls, year):
        """Return fixed date of Hebrew new year 'year'."""
        return cls.EPOCH + cls.elapsed_days(year) + cls.year_length_correction(year)
    
    @classmethod
    def year_length_correction(cls, year):
        """Return delays to start of Hebrew year 'year' to keep ordinary
        year in range 353-356 and leap year in range 383-386."""
        # I had a bug... h_year = 1 instead of h_year - 1!!!
        ny0 = cls.elapsed_days(year - 1)
        ny1 = cls.elapsed_days(year)
        ny2 = cls.elapsed_days(year + 1)
        if ny2 - ny1 == 356:
            return 2
        elif ny1 - ny0 == 382:
            return 1
        else:
            return 0

    @classmethod    
    def days_in_year(cls, year):
        """Return number of days in Hebrew year 'year'."""
        return cls.new_year(year + 1) - cls.new_year(year)

    @classmethod    
    def is_long_marheshvan(cls, year):
        """Return True if Marheshvan is long in Hebrew year 'year'."""
        return cls.days_in_year(year) in (355, 385)

    @classmethod    
    def is_short_kislev(cls, year):
        """Return True if Kislev is short in Hebrew year 'year'."""
        return cls.days_in_year(year) in (353, 383)

    @classmethod    
    def yom_kippur(cls, gregorian_year):
        """Return fixed date of Yom Kippur occurring in Gregorian year 'gregorian_year'."""
        hebrew_year = gregorian_year - GregorianDate.to_year(cls.EPOCH) + 1
        return HebrewDate(hebrew_year, HebrewMonth.TISHRI, 10).to_fixed()
    
    @classmethod    
    def passover(cls, gregorian_year):
        """Return fixed date of Passover occurring in Gregorian year 'gregorian_year'."""
        hebrew_year = gregorian_year - GregorianDate.to_year(cls.EPOCH)
        return HebrewDate(hebrew_year, HebrewMonth.NISAN, 15).to_fixed()
   
    @classmethod    
    def omer(cls, fixed_date):
        """Return the number of elapsed weeks and days in the omer at date fixed_date.
        Throws ValueError if that date does not fall during the omer."""
        c = fixed_date - cls.passover(GregorianDate.to_year(fixed_date))
        if 1 <= c <= 49:
            return [quotient(c, 7), mod(c, 7)]
        else:
            raise ValueError("Date does not fall within omer")

    @classmethod   
    def purim(cls, gregorian_year):
        """Return fixed date of Purim occurring in Gregorian year 'gregorian_year'."""
        hebrew_year = gregorian_year - GregorianDate.to_year(cls.EPOCH)
        last_month  = cls.last_month_of_year(hebrew_year)
        return HebrewDate(hebrew_year, last_month, 14).to_fixed()

    @classmethod    
    def ta_anit_esther(cls, gregorian_year):
        """Return fixed date of Ta'anit Esther occurring in Gregorian
        year 'gregorian_year'."""
        purim_date = cls.purim(gregorian_year)
        return purim_date - 3 if DayOfWeek.from_fixed(purim_date) == DayOfWeek.Sunday else purim_date - 1
    
    @classmethod
    def tishah_be_av(cls, gregorian_year):
        """Return fixed date of Tishah be_Av occurring in Gregorian year 'gregorian_year'."""
        hebrew_year = gregorian_year - GregorianDate.to_year(cls.EPOCH)
        av9 = HebrewDate(hebrew_year, HebrewMonth.AV, 9).to_fixed()
        return av9 + 1 if DayOfWeek.from_fixed(av9) == DayOfWeek.Saturday else av9

    @classmethod    
    def birkath_ha_hama(cls, gregorian_year):
        """Return the list of fixed date of Birkath ha_Hama occurring in
        Gregorian year 'gregorian_year', if it occurs."""
        dates = CopticDate.in_gregorian(7, 30, gregorian_year)
        return (dates
                if ((not (dates == [])) and
                    (mod(CopticDate.from_fixed(dates[0]).year, 28) == 17))
                else [])
    
    @classmethod
    def sh_ela(cls, gregorian_year):
        """Return the list of fixed dates of Sh'ela occurring in
        Gregorian year 'gregorian_year'."""
        return CopticDate.in_gregorian(3, 26, gregorian_year)
    
    @classmethod
    def in_gregorian(cls, month, day, gregorian_year):
        """Return list of the fixed dates of Hebrew month, 'month', day, 'day',
        that occur in Gregorian year 'gregorian_year'."""
        jan1  = GregorianDate.new_year(gregorian_year)
        y     = HebrewDate.from_fixed(jan1).year
        date1 = HebrewDate(y, month, day).to_fixed()
        date2 = HebrewDate(y + 1, month, day).to_fixed()
        # Hebrew and Gregorian calendar are aligned but certain
        # holidays, i.e. Tzom Tevet, can fall on either side of Jan 1.
        # So we can have 0, 1 or 2 occurences of that holiday.
        dates = [date1, date2]
        return list_range(dates, GregorianDate.year_range(gregorian_year))
    
    @classmethod
    def tzom_tevet(cls, gregorian_year):
        """Return the list of fixed dates for Tzom Tevet (Tevet 10) that
        occur in Gregorian year 'gregorian_year'. It can occur 0, 1 or 2 times per
        Gregorian year."""
        jan1  = GregorianDate.new_year(gregorian_year)
        y     = HebrewDate.from_fixed(jan1).year
        d1 = HebrewDate(y, HebrewMonth.TEVET, 10).to_fixed()
        d1 = d1 + 1 if DayOfWeek.from_fixed(d1) == DayOfWeek.Saturday else d1
        d2 = HebrewDate(y + 1, HebrewMonth.TEVET, 10).to_fixed()
        d2 = d2 + 1 if DayOfWeek.from_fixed(d2) == DayOfWeek.Saturday else d2
        dates = [d1, d2]
        return list_range(dates, GregorianDate.year_range(gregorian_year))
    
    # this is a simplified version where no check for SATURDAY
    # is performed: from hebrew year 1 till 2000000
    # there is no TEVET 10 falling on Saturday...
    @classmethod
    def alt_tzom_tevet(cls, gregorian_year):
        """Return the list of fixed dates for Tzom Tevet (Tevet 10) that
        occur in Gregorian year 'gregorian_year'. It can occur 0, 1 or 2 times per
        Gregorian year."""
        return cls.in_gregorian(HebrewMonth.TEVET, 10, gregorian_year)

    @classmethod    
    def yom_ha_zikkaron(cls, gregorian_year):
        """Return fixed date of Yom ha_Zikkaron occurring in Gregorian
        year 'gregorian_year'."""
        hebrew_year = gregorian_year - GregorianDate.to_year(cls.EPOCH)
        iyyar4 = HebrewDate(hebrew_year, HebrewMonth.IYYAR, 4).to_fixed()
        
        if DayOfWeek.from_fixed(iyyar4) in (DayOfWeek.Thursday, DayOfWeek.Friday):
            return DayOfWeek.Wednesday.before(iyyar4)
        elif DayOfWeek.Sunday == DayOfWeek.from_fixed(iyyar4):
            return iyyar4 + 1
        else:
            return iyyar4

    def birthday(self, year):
        """Return fixed date of the anniversary of Hebrew birth date
        birthdate occurring in Hebrew year."""
        if self.month == self.last_month_of_year(self.year):
            return HebrewDate(year, self.last_month_of_year(year), self.day).to_fixed()
        else:
            return HebrewDate(year, self.month, 1).to_fixed() + self.day - 1
    
    def birthday_in_gregorian(self, gregorian_year):
        """Return the list of the fixed dates of Hebrew birthday
        birthday that occur in Gregorian 'gregorian_year'."""
        jan1 = GregorianDate.new_year(gregorian_year)
        y    = HebrewDate.from_fixed(jan1).year
        date1 = self.birthday(y)
        date2 = self.birthday(y + 1)
        return list_range([date1, date2], GregorianDate.year_range(gregorian_year))

    def yahrzeit(self, year):
        """Return fixed date of the anniversary of Hebrew death date
        occurring in Hebrew 'year'."""
    
        if self.month == HebrewMonth.MARHESHVAN and self.day == 30 and not self.is_long_marheshvan(self.year + 1):
            return HebrewDate(year, HebrewMonth.KISLEV, 1).to_fixed() - 1
        elif self.month == HebrewMonth.KISLEV and self.day == 30 and self.is_short_kislev(self.year + 1):
            return HebrewDate(year, HebrewMonth.TEVET, 1).to_fixed() - 1
        elif self.month == HebrewMonth.ADARII:
            return HebrewDate(year, self.last_month_of_year(year), self.day).to_fixed()
        elif self.day == 30 and self.month == HebrewMonth.ADAR and not self.is_leap_year(year):
            return HebrewDate(year, HebrewMonth.SHEVAT, 30).to_fixed()
        else:
            return HebrewDate(year, self.month, 1).to_fixed() + self.day - 1

    def yahrzeit_in_gregorian(self, gregorian_year):
        """Return the list of the fixed dates of death date death_date (yahrzeit)
        that occur in Gregorian year 'gregorian_year'."""
        jan1 = GregorianDate.new_year(gregorian_year)
        y    = HebrewDate.from_fixed(jan1).year
        date1 = self.yahrzeit(y)
        date2 = self.yahrzeit(y + 1)
        return list_range([date1, date2], GregorianDate.year_range(gregorian_year))
    
    @classmethod    
    def possible_days(cls, month, day):
        """Return a list of possible days of week for Hebrew day 'day'
        and Hebrew month 'month'."""
        h_date0 = HebrewDate(5, HebrewMonth.NISAN, 1)
        h_year  = 6 if month > HebrewMonth.ELUL else 5
        h_date  = HebrewDate(h_year, month, day)
        n       = h_date.to_fixed() - h_date0.to_fixed()
        basic   = [DayOfWeek.Tuesday, DayOfWeek.Thursday, DayOfWeek.Saturday]
    
        if month == HebrewMonth.MARHESHVAN and day == 30:
            extra = []
        elif (month == HebrewMonth.KISLEV) and (day < 30):
            extra = [DayOfWeek.Monday, DayOfWeek.Wednesday, DayOfWeek.Friday]
        elif (month == HebrewMonth.KISLEV) and (day == 30):
            extra = [DayOfWeek.Monday]
        elif month in [HebrewMonth.TEVET, HebrewMonth.SHEVAT]:
            extra = [DayOfWeek.Sunday, DayOfWeek.Monday]
        elif (month == HebrewMonth.ADAR) and (day < 30):
            extra = [DayOfWeek.Sunday, DayOfWeek.Monday]
        else:
            extra = [DayOfWeek.Sunday]
    
        basic.extend(extra)
        return map(lambda x: DayOfWeek.from_fixed(x + n), basic)

# see lines 5940-5955 in calendrica-3.0.cl
def observational_hebrew_new_year(g_year):
    """Return fixed date of Observational (classical)
    Nisan 1 occurring in Gregorian year, g_year."""
    jan1 = GregorianDate.new_year(g_year)
    equinox = Solar.solar_longitude_after(Astro.SPRING, jan1)
    sset = JAFFA.universal_from_standard(JAFFA.sunset(ifloor(equinox)))
    return phasis_on_or_after(ifloor(equinox) - (14 if (equinox < sset) else 13), JAFFA)

# see lines 5957-5973 in calendrica-3.0.cl
def fixed_from_observational_hebrew(h_date):
    """Return fixed date equivalent to Observational Hebrew date."""
    year1 = (h_date.year - 1) if (h_date.month >= HebrewMonth.TISHRI) else h_date.year
    start = HebrewDate(year1, HebrewMonth.NISAN, 1).to_fixed()
    g_year = GregorianDate.to_year(start + 60)
    new_year = observational_hebrew_new_year(g_year)
    midmonth = new_year + iround(29.5 * (h_date.month - 1)) + 15
    return JAFFA.phasis_on_or_before(midmonth) + h_date.day - 1

# see lines 5975-5991 in calendrica-3.0.cl
def observational_hebrew_from_fixed(date):
    """Return Observational Hebrew date (year month day)
    corresponding to fixed date, date."""
    crescent = JAFFA.phasis_on_or_before(date)
    g_year = GregorianDate.to_year(date)
    ny = observational_hebrew_new_year(g_year)
    new_year = observational_hebrew_new_year(g_year - 1) if (date < ny) else ny
    month = iround((crescent - new_year) / 29.5) + 1
    year = (HebrewDate.from_fixed(new_year).year +
            (1 if (month >= HebrewMonth.TISHRI) else 0))
    day = date - crescent + 1
    return HebrewDate(year, month, day)

# see lines 5993-5997 in calendrica-3.0.cl
def classical_passover_eve(g_year):
    """Return fixed date of Classical (observational) Passover Eve
    (Nisan 14) occurring in Gregorian year, g_year."""
    return observational_hebrew_new_year(g_year) + 13

# see lines 5920-5923 in calendrica-3.0.cl
JAFFA = Location(angle(32, 1, 60), angle(34, 45, 0), 0, Clock.days_from_hours(2))

# see lines 5925-5938 in calendrica-3.0.cl
def phasis_on_or_after(date, location):
    """Return closest fixed date on or after date, date, on the eve
    of which crescent moon first became visible at location, location."""
    mean = date - ifloor(Lunar.lunar_phase(date + 1) / mpf(360) * Lunar.MEAN_SYNODIC_MONTH)
    tau = (date if (((date - mean) <= 3) and
                    (not location.visible_crescent(date - 1)))
           else (mean + 29))
    return next_int(tau, lambda d: location.visible_crescent(d))
