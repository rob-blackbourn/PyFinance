from operator import mod
from enum import IntEnum
from mpmath import mpf
from py_cal_cal import quotient, summa, iround, ifloor, final_int, next_int, list_range, angle
from day_arithmatic import DayOfWeek
from astro import phasis_on_or_before, solar_longitude_after, SPRING, lunar_phase, MEAN_SYNODIC_MONTH, visible_crescent
from julian_calendars import JulianDate
from coptic_calendars import CopticDate
from location import Location
from gregorian_calendars import GregorianDate, JulianMonth
from time_arithmatic import Clock

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
    
class HebrewDate(object):

    EPOCH = JulianDate(JulianDate.bce(3761),  JulianMonth.October, 7).to_fixed()
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

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
        if ((month in [HebrewMonth.IYYAR, HebrewMonth.TAMMUZ, HebrewMonth.ELUL, HebrewMonth.TEVET, HebrewMonth.ADARII])
            or ((month == HebrewMonth.ADAR) and (not cls.is_leap_year(year)))
            or ((month == HebrewMonth.MARHESHVAN) and (not cls.is_long_marheshvan(year)))
            or ((month == HebrewMonth.KISLEV) and cls.is_short_kislev(year))):
            return 29
        else:
            return 30

    @classmethod    
    def molad(cls, month, year):
        """Return moment of mean conjunction of month in Hebrew year."""
        y = (year + 1) if (month < HebrewMonth.TISHRI) else year
        months_elapsed = month - HebrewMonth.TISHRI + quotient(235 * y - 234, 19)
        return (cls.EPOCH -
               876/25920 +
               months_elapsed * (29 + Clock.days_from_hours(12) + 793/25920))

    @classmethod    
    def elapsed_days(cls, year):
        """Return number of days elapsed from the (Sunday) noon prior
        to the epoch of the Hebrew calendar to the mean
        conjunction (molad) of Tishri of Hebrew year h_year,
        or one day later."""
        months_elapsed = quotient(235 * year - 234, 19)
        parts_elapsed  = 12084 + 13753 * months_elapsed
        days = 29 * months_elapsed + quotient(parts_elapsed, 25920)
        return   (days + 1) if (mod(3 * (days + 1), 7) < 3) else days

    @classmethod    
    def hebrew_new_year(cls, year):
        """Return fixed date of Hebrew new year h_year."""
        return (cls.EPOCH +
               cls.elapsed_days(year) +
               cls.year_length_correction(year))
    
    @classmethod
    def year_length_correction(cls, year):
        """Return delays to start of Hebrew year h_year to keep ordinary
        year in range 353-356 and leap year in range 383-386."""
        # I had a bug... h_year = 1 instead of h_year - 1!!!
        ny0 = cls.elapsed_days(year - 1)
        ny1 = cls.elapsed_days(year)
        ny2 = cls.elapsed_days(year + 1)
        if ((ny2 - ny1) == 356):
            return 2
        elif ((ny1 - ny0) == 382):
            return 1
        else:
            return 0

    @classmethod    
    def days_in_year(cls, year):
        """Return number of days in Hebrew year h_year."""
        return cls.new_year(year + 1) - cls.new_year(year)

    @classmethod    
    def is_long_marheshvan(cls, year):
        """Return True if Marheshvan is long in Hebrew year h_year."""
        return cls.days_in_year(year) in [355, 385]

    @classmethod    
    def is_short_kislev(cls, year):
        """Return True if Kislev is short in Hebrew year h_year."""
        return cls.days_in_year(year) in [353, 383]
    
    def to_fixed(self):
        """Return fixed date of Hebrew date h_date."""
        if (self.month < HebrewMonth.TISHRI):
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
    def hebrew_from_fixed(cls, date):
        """Return  Hebrew (year month day) corresponding to fixed date date.
        # The fraction can be approximated by 365.25."""
        approx = quotient(date - cls.EPOCH, 35975351/98496) + 1
        year = final_int(approx - 1, lambda y: cls.new_year(y) <= date)
        start = (HebrewMonth.TISHRI
                 if (date < HebrewDate(year, HebrewMonth.NISAN, 1).to_fixed())
                 else  HebrewMonth.NISAN)
        month = next_int(start, lambda m: date <= HebrewDate(year, m, cls.last_day_of_month(m, year)).to_fixed())
        day = date - HebrewDate(year, month, 1).to_fixed() + 1
        return HebrewDate(year, month, day)

    @classmethod    
    def yom_kippur(cls, year):
        """Return fixed date of Yom Kippur occurring in Gregorian year."""
        hebrew_year = year - GregorianDate.to_year(cls.EPOCH) + 1
        return HebrewDate(hebrew_year, HebrewMonth.TISHRI, 10).to_fixed()
    
    @classmethod    
    def passover(cls, year):
        """Return fixed date of Passover occurring in Gregorian year g_year."""
        hebrew_year = year - GregorianDate.to_year(cls.EPOCH)
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
    def purim(cls, g_year):
        """Return fixed date of Purim occurring in Gregorian year g_year."""
        hebrew_year = g_year - GregorianDate.to_year(cls.EPOCH)
        last_month  = cls.last_month_of_year(hebrew_year)
        return HebrewDate(hebrew_year, last_month, 14).to_fixed()

    @classmethod    
    def ta_anit_esther(cls, g_year):
        """Return fixed date of Ta'anit Esther occurring in Gregorian
        year g_year."""
        purim_date = cls.purim(g_year)
        return ((purim_date - 3)
                if (DayOfWeek.from_fixed(purim_date) == DayOfWeek.Sunday)
                else (purim_date - 1))
    
    @classmethod
    def tishah_be_av(cls, g_year):
        """Return fixed date of Tishah be_Av occurring in Gregorian year g_year."""
        hebrew_year = g_year - GregorianDate.to_year(cls.EPOCH)
        av9 = HebrewDate(hebrew_year, HebrewMonth.AV, 9).to_fixed()
        return (av9 + 1) if (DayOfWeek.from_fixed(av9) == DayOfWeek.Saturday) else av9

    @classmethod    
    def birkath_ha_hama(cls, g_year):
        """Return the list of fixed date of Birkath ha_Hama occurring in
        Gregorian year g_year, if it occurs."""
        dates = CopticDate.in_gregorian(7, 30, g_year)
        return (dates
                if ((not (dates == [])) and
                    (mod(CopticDate.from_fixed(dates[0]).year, 28) == 17))
                else [])
    
    @classmethod
    def sh_ela(cls, g_year):
        """Return the list of fixed dates of Sh'ela occurring in
        Gregorian year g_year."""
        return CopticDate.in_gregorian(3, 26, g_year)
    
    @classmethod
    def in_gregorian(cls, h_month, h_day, g_year):
        """Return list of the fixed dates of Hebrew month, h_month, day, h_day,
        that occur in Gregorian year g_year."""
        jan1  = GregorianDate.new_year(g_year)
        y     = HebrewDate.from_fixed(jan1).year
        date1 = HebrewDate(y, h_month, h_day).to_fixed()
        date2 = HebrewDate(y + 1, h_month, h_day).to_fixed()
        # Hebrew and Gregorian calendar are aligned but certain
        # holidays, i.e. Tzom Tevet, can fall on either side of Jan 1.
        # So we can have 0, 1 or 2 occurences of that holiday.
        dates = [date1, date2]
        return list_range(dates, GregorianDate.year_range(g_year))
    
    @classmethod
    def tzom_tevet(cls, g_year):
        """Return the list of fixed dates for Tzom Tevet (Tevet 10) that
        occur in Gregorian year g_year. It can occur 0, 1 or 2 times per
        Gregorian year."""
        jan1  = GregorianDate.new_year(g_year)
        y     = HebrewDate.from_fixed(jan1).year
        d1 = HebrewDate(y, HebrewMonth.TEVET, 10).to_fixed()
        d1 = (d1 + 1) if (DayOfWeek.from_fixed(d1) == DayOfWeek.Saturday) else d1
        d2 = HebrewDate(y + 1, HebrewMonth.TEVET, 10).to_fixed()
        d2 = (d2 + 1) if (DayOfWeek.from_fixed(d2) == DayOfWeek.Saturday) else d2
        dates = [d1, d2]
        return list_range(dates, GregorianDate.year_range(g_year))
    
    # this is a simplified version where no check for SATURDAY
    # is performed: from hebrew year 1 till 2000000
    # there is no TEVET 10 falling on Saturday...
    @classmethod
    def alt_tzom_tevet(cls, g_year):
        """Return the list of fixed dates for Tzom Tevet (Tevet 10) that
        occur in Gregorian year g_year. It can occur 0, 1 or 2 times per
        Gregorian year."""
        return cls.in_gregorian(HebrewMonth.TEVET, 10, g_year)

    @classmethod    
    def yom_ha_zikkaron(cls, g_year):
        """Return fixed date of Yom ha_Zikkaron occurring in Gregorian
        year g_year."""
        hebrew_year = g_year - GregorianDate.to_year(cls.EPOCH)
        iyyar4 = HebrewDate(hebrew_year, HebrewMonth.IYYAR, 4).to_fixed()
        
        if (DayOfWeek.from_fixed(iyyar4) in [DayOfWeek.Thursday, DayOfWeek.Friday]):
            return DayOfWeek(DayOfWeek.Wednesday).before(iyyar4)
        elif (DayOfWeek.Sunday == DayOfWeek.from_fixed(iyyar4)):
            return iyyar4 + 1
        else:
            return iyyar4

    @classmethod    
    def birthday(cls, birthdate, year):
        """Return fixed date of the anniversary of Hebrew birth date
        birthdate occurring in Hebrew year."""
        if (birthdate.month == cls.last_month_of_year(birthdate.year)):
            return HebrewDate(year, cls.last_month_of_year(year), birthdate.day).to_fixed()
        else:
            return HebrewDate(year, birthdate.month, 1).to_fixed() + birthdate.day - 1
    
    @classmethod
    def birthday_in_gregorian(cls, birthdate, g_year):
        """Return the list of the fixed dates of Hebrew birthday
        birthday that occur in Gregorian g_year."""
        jan1 = GregorianDate.new_year(g_year)
        y    = HebrewDate.from_fixed(jan1).year
        date1 = cls.birthday(birthdate, y)
        date2 = cls.birthday(birthdate, y + 1)
        return list_range([date1, date2], GregorianDate.year_range(g_year))

    @classmethod    
    def yahrzeit(cls, death_date, h_year):
        """Return fixed date of the anniversary of Hebrew death date death_date
        occurring in Hebrew h_year."""
    
        if ((death_date.month == HebrewMonth.MARHESHVAN) and
            (death_date.day == 30) and
            (not cls.is_long_marheshvan(death_date.year + 1))):
            return HebrewDate(h_year, HebrewMonth.KISLEV, 1).to_fixed() - 1
        elif ((death_date.month == HebrewMonth.KISLEV) and
              (death_date.day == 30) and
              cls.is_short_kislev(death_date.year + 1)):
            return HebrewDate(h_year, HebrewMonth.TEVET, 1).to_fixed() - 1
        elif (death_date.month == HebrewMonth.ADARII):
            return HebrewDate(h_year, cls.last_month_of_year(h_year), death_date.day).to_fixed()
        elif ((death_date.day == 30) and
              (death_date.month == HebrewMonth.ADAR) and
              (not cls.is_leap_year(h_year))):
            return HebrewDate(h_year, HebrewMonth.SHEVAT, 30).to_fixed()
        else:
            return HebrewDate(h_year, death_date.month, 1).to_fixed() + death_date.day - 1

    @classmethod    
    def yahrzeit_in_gregorian(cls, death_date, g_year):
        """Return the list of the fixed dates of death date death_date (yahrzeit)
        that occur in Gregorian year g_year."""
        jan1 = GregorianDate.new_year(g_year)
        y    = HebrewDate.from_fixed(jan1).year
        date1 = cls.yahrzeit(death_date, y)
        date2 = cls.yahrzeit(death_date, y + 1)
        return list_range([date1, date2], GregorianDate.year_range(g_year))
    
    @classmethod    
    def possible_hebrew_days(cls, h_month, h_day):
        """Return a list of possible days of week for Hebrew day h_day
        and Hebrew month h_month."""
        h_date0 = HebrewDate(5, HebrewMonth.NISAN, 1)
        h_year  = 6 if (h_month > HebrewMonth.ELUL) else 5
        h_date  = HebrewDate(h_year, h_month, h_day)
        n       = h_date.to_fixed() - h_date0.to_fixed()
        basic   = [DayOfWeek.Tuesday, DayOfWeek.Thursday, DayOfWeek.Saturday]
    
        if (h_month == HebrewMonth.MARHESHVAN) and (h_day == 30):
            extra = []
        elif (h_month == HebrewMonth.KISLEV) and (h_day < 30):
            extra = [DayOfWeek.Monday, DayOfWeek.Wednesday, DayOfWeek.Friday]
        elif (h_month == HebrewMonth.KISLEV) and (h_day == 30):
            extra = [DayOfWeek.Monday]
        elif h_month in [HebrewMonth.TEVET, HebrewMonth.SHEVAT]:
            extra = [DayOfWeek.Sunday, DayOfWeek.Monday]
        elif (h_month == HebrewMonth.ADAR) and (h_day < 30):
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
    equinox = solar_longitude_after(SPRING, jan1)
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
    return phasis_on_or_before(midmonth, JAFFA) + h_date.day - 1

# see lines 5975-5991 in calendrica-3.0.cl
def observational_hebrew_from_fixed(date):
    """Return Observational Hebrew date (year month day)
    corresponding to fixed date, date."""
    crescent = phasis_on_or_before(date, JAFFA)
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
    mean = date - ifloor(lunar_phase(date + 1) / mpf(360) *
                        MEAN_SYNODIC_MONTH)
    tau = (date if (((date - mean) <= 3) and
                    (not visible_crescent(date - 1, location)))
           else (mean + 29))
    return next_int(tau, lambda d: visible_crescent(d, location))
