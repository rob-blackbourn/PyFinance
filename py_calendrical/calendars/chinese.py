from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.py_cal_cal import ifloor, amod, quotient, iround, iceiling, rd
from py_calendrical.triganometry import angle
from py_calendrical.location import Location
from py_calendrical.time_arithmatic import Clock
from py_calendrical.utils import next_int
from py_calendrical.solar import Solar
from py_calendrical.astro import Astro
from py_calendrical.lunar import Lunar

class ChineseDate(object):

    EPOCH = GregorianDate(-2636, JulianMonth.February, 15).to_fixed()
    
    def __init__(self, cycle, year, month, leap, day):
        self.cycle = cycle
        self.year = year
        self.month = month
        self.leap = leap
        self.day = day
    
    def to_fixed(self):
        """Return fixed date of Chinese date, c_date."""
        mid_year = ifloor(self.EPOCH + ((((self.cycle - 1) * 60) + (self.year - 1) + 1/2) * Solar.MEAN_TROPICAL_YEAR))
        new_year = self.new_year_on_or_before(mid_year)
        p = self.new_moon_on_or_after(new_year + ((self.month - 1) * 29))
        d = self.from_fixed(p)
        prior_new_moon = (p if ((self.month == d.month) and (self.leap == d.leap)) else self.new_moon_on_or_after(1 + p))
        return prior_new_moon + self.day - 1

    @classmethod    
    def from_fixed(cls, fixed_date):
        """Return Chinese date (cycle year month leap day) of fixed date, 'fixed_date'."""
        s1 = cls.winter_solstice_on_or_before(fixed_date)
        s2 = cls.winter_solstice_on_or_before(s1 + 370)
        next_m11 = cls.new_moon_before(1 + s2)
        m12 = cls.new_moon_on_or_after(1 + s1)
        leap_year = iround((next_m11 - m12) / Lunar.MEAN_SYNODIC_MONTH) == 12
    
        m = cls.new_moon_before(1 + fixed_date)
        month = amod(iround((m - m12) / Lunar.MEAN_SYNODIC_MONTH) - (1 if (leap_year and cls.is_prior_leap_month(m12, m)) else 0), 12)
        leap_month = (leap_year and cls.is_no_major_solar_term(m) and (not cls.is_prior_leap_month(m12, cls.new_moon_before(m))))
        elapsed_years = (ifloor(mpf(1.5) - (month / 12) + ((fixed_date - cls.EPOCH) / Solar.MEAN_TROPICAL_YEAR)))
        cycle = 1 + quotient(elapsed_years - 1, 60)
        year = amod(elapsed_years, 60)
        day = 1 + (fixed_date - m)
        return ChineseDate(cycle, year, month, leap_month, day)

    @classmethod        
    def location(cls, tee):
        """Return location of Beijing; time zone varies with time, tee."""
        year = GregorianDate.to_year(ifloor(tee))
        if (year < 1929):
            return Location(angle(39, 55, 0), angle(116, 25, 0), 43.5, Clock.days_from_hours(1397/180))
        else:
            return Location(angle(39, 55, 0), angle(116, 25, 0), 43.5, Clock.days_from_hours(8))

    @classmethod
    def solar_longitude_on_or_after(cls, lam, fixed_date):
        """Return moment (Beijing time) of the first date on or after
        fixed date, 'fixed_date', (Beijing time) when the solar longitude
        will be 'lam' degrees."""
        tee = Solar.solar_longitude_after(lam, cls.location(fixed_date).universal_from_standard(fixed_date))
        return cls.location(tee).standard_from_universal(tee)

    @classmethod
    def major_solar_term(cls, fixed_date):
        """Return last Chinese major solar term (zhongqi) before
        fixed date, 'fixed_date'."""
        s = Solar.solar_longitude(cls.location(fixed_date).universal_from_standard(fixed_date))
        return amod(2 + quotient(int(s), 30), 12)

    @classmethod
    def major_solar_term_on_or_after(cls, fixed_date):
        """Return moment (in Beijing) of the first Chinese major
        solar term (zhongqi) on or after fixed date, 'fixed_date'.  The
        major terms begin when the sun's longitude is a
        multiple of 30 degrees."""
        s = Solar.solar_longitude(cls.midnight(fixed_date))
        l = mod(30 * iceiling(s / 30), 360)
        return cls.solar_longitude_on_or_after(l, fixed_date)

    @classmethod    
    def current_minor_solar_term(cls, fixed_date):
        """Return last Chinese minor solar term (jieqi) before date, 'fixed_date'."""
        s = Solar.solar_longitude(cls.location(fixed_date).universal_from_standard(fixed_date))
        return amod(3 + quotient(s - 15, 30), 12)

    @classmethod    
    def minor_solar_term_on_or_after(cls, fixed_date):
        """Return moment (in Beijing) of the first Chinese minor solar
        term (jieqi) on or after fixed date, 'fixed_date'.  The minor terms
        begin when the sun's longitude is an odd multiple of 15 degrees."""
        s = Solar.solar_longitude(cls.midnight(fixed_date))
        l = mod(30 * iceiling((s - 15) / 30) + 15, 360)
        return cls.solar_longitude_on_or_after(l, fixed_date)

    @classmethod    
    def new_moon_before(cls, fixed_date):
        """Return fixed date (Beijing) of first new moon before fixed date, 'fixed_date'."""
        tee = Lunar.new_moon_before(cls.midnight(fixed_date))
        return ifloor(cls.location(tee).standard_from_universal(tee))
    
    @classmethod    
    def new_moon_on_or_after(cls, fixed_date):
        """Return fixed date (Beijing) of first new moon on or after
        fixed date, 'fixed_date'."""
        tee = Lunar.new_moon_at_or_after(cls.midnight(fixed_date))
        return ifloor(cls.chinese_location(tee).standard_from_universal(tee))

    @classmethod    
    def is_no_major_solar_term(cls, fixed_date):
        """Return True if Chinese lunar month starting on date, 'fixed_date',
        has no major solar term."""
        return (cls.current_major_solar_term(fixed_date) ==
                cls.current_major_solar_term(cls.new_moon_on_or_after(fixed_date + 1)))

    @classmethod    
    def midnight(cls, fixed_date):
        """Return Universal time of (clock) midnight at start of fixed
        date, 'fixed_date', in China."""
        return cls.location(fixed_date).universal_from_standard(fixed_date)

    @classmethod    
    def winter_solstice_on_or_before(cls, fixed_date):
        """Return fixed date, in the Chinese zone, of winter solstice
        on or before fixed date, 'fixed_date'."""
        approx = Solar.estimate_prior_solar_longitude(Astro.WINTER, cls.midnight(fixed_date + 1))
        return next_int(ifloor(approx) - 1, lambda day: Astro.WINTER < Solar.solar_longitude(cls.midnight(1 + day)))
    
    @classmethod    
    def new_year_in_sui(cls, fixed_date):
        """Return fixed date of Chinese New Year in sui (period from
        solstice to solstice) containing date, 'fixed_date'."""
        s1 = cls.winter_solstice_on_or_before(fixed_date)
        s2 = cls.winter_solstice_on_or_before(s1 + 370)
        next_m11 = cls.new_moon_before(1 + s2)
        m12 = cls.new_moon_on_or_after(1 + s1)
        m13 = cls.new_moon_on_or_after(1 + m12)
        leap_year = iround((next_m11 - m12) / Lunar.MEAN_SYNODIC_MONTH) == 12
    
        if (leap_year and
            (cls.is_no_major_solar_term(m12) or cls.is_no_major_solar_term(m13))):
            return cls.new_moon_on_or_after(1 + m13)
        else:
            return m13

    @classmethod
    def new_year_on_or_before(cls, fixed_date):
        """Return fixed date of Chinese New Year on or before fixed date, 'fixed_date'."""
        new_year = cls.new_year_in_sui(fixed_date)
        if (fixed_date >= new_year):
            return new_year
        else:
            return cls.new_year_in_sui(fixed_date - 180)

    @classmethod    
    def new_year(cls, gregorian_year):
        """Return fixed date of Chinese New Year in Gregorian year, 'gregorian_year'."""
        return cls.new_year_on_or_before(GregorianDate(gregorian_year, JulianMonth.July, 1).to_fixed())

    @classmethod
    def is_prior_leap_month(cls, m_prime, m):
        """Return True if there is a Chinese leap month on or after lunar
        month starting on fixed day, m_prime and at or before
        lunar month starting at fixed date, m."""
        return ((m >= m_prime) and
                (cls.is_no_major_solar_term(m) or
                 cls.is_prior_leap_month(m_prime, cls.new_moon_before(m))))

    @classmethod
    def dragon_festival(cls, gregorian_year):
        """Return fixed date of the Dragon Festival occurring in Gregorian
        year 'gregorian_year'."""
        elapsed_years = 1 + gregorian_year - GregorianDate.to_year(cls.EPOCH)
        cycle = 1 + quotient(elapsed_years - 1, 60)
        year = amod(elapsed_years, 60)
        return ChineseDate(cycle, year, 5, False, 5).to_fixed()

    @classmethod
    def qing_ming(cls, gregorian_year):
        """Return fixed date of Qingming occurring in Gregorian year, 'gregorian_year'."""
        return ifloor(cls.minor_solar_term_on_or_after(
            GregorianDate(gregorian_year, JulianMonth.March, 30).to_fixed()))

    def age(self, fixed_date):
        """Return the age at fixed date, date, given Chinese birthdate, birthdate,
        according to the Chinese custom.
        Raises ValueError if date is before birthdate."""
        today = self.from_fixed(fixed_date)
        if (fixed_date >= self.to_fixed()):
            return (60 * (today.cycle - self.cycle) + (today.year -  self.year) + 1)
        else:
            raise ValueError("fixed_date is before birthdate")
    
    @classmethod    
    def year_marriage_augury(cls, cycle, year):
        """Return the marriage augury type of Chinese year, year in cycle, cycle.
        0 means lichun does not occur (widow or double-blind years),
        1 means it occurs once at the end (blind),
        2 means it occurs once at the start (bright), and
        3 means it occurs twice (double-bright or double-happiness)."""
        new_year = ChineseDate(cycle, year, 1, False, 1).to_fixed()
        c = (cycle + 1) if (year == 60) else cycle
        y = 1 if (year == 60) else (year + 1)
        next_new_year = ChineseDate(c, y, 1, False, 1).to_fixed()
        first_minor_term = cls.current_minor_solar_term(new_year)
        next_first_minor_term = cls.current_minor_solar_term(next_new_year)
        if ((first_minor_term == 1) and (next_first_minor_term == 12)):
            res = 0
        elif ((first_minor_term == 1) and (next_first_minor_term != 12)):
            res = 1
        elif ((first_minor_term != 1) and (next_first_minor_term == 12)):
            res = 2
        else:
            res = 3
        return res

class ChineseName(object):

    MONTH_NAME_EPOCH = 57
    DAY_NAME_EPOCH = rd(45)
    
    def __init__(self, stem, branch):
        if (mod(stem, 2) != mod(branch, 2)):
            raise ValueError("Combination/branch combination is not possible")
        self.stem = stem
        self.branch = branch
        
    @classmethod
    def sexagesimal_name(n):
        """Return the n_th name of the Chinese sexagesimal cycle."""
        return ChineseName(amod(n, 10), amod(n, 12))

    @classmethod
    def chinese_name_difference(cls, c_name1, c_name2):
        """Return the number of names from Chinese name c_name1 to the
        next occurrence of Chinese name c_name2."""
        stem_difference   = c_name2.stem - c_name1.stem
        branch_difference = c_name2.branch - c_name1.branch
        return 1 + mod(stem_difference - 1 + 25 * (branch_difference - stem_difference), 60)

    @classmethod
    def year_name(cls, year):
        """Return sexagesimal name for Chinese year, year, of any cycle."""
        return cls.sexagesimal_name(year)

    @classmethod
    def month_name(cls, month, year):
        """Return sexagesimal name for month, month, of Chinese year, year."""
        elapsed_months = (12 * (year - 1)) + (month - 1)
        return cls.sexagesimal_name(elapsed_months - cls.MONTH_NAME_EPOCH)

    @classmethod
    def day_name(cls, date):
        """Return Chinese sexagesimal name for date, date."""
        return cls.sexagesimal_name(date - cls.DAY_NAME_EPOCH)

    @classmethod
    def day_name_on_or_before(cls, name, date):
        """Return fixed date of latest date on or before fixed date, date, that
        has Chinese name, name."""
        return (date - mod(date + cls.name_difference(name, cls.sexagesimal_name(cls.DAY_NAME_EPOCH)), 60))

def japanese_location(tee):
    """Return the location for Japanese calendar; varies with moment, tee."""
    year = GregorianDate.to_year(ifloor(tee))
    if (year < 1888):
        # Tokyo (139 deg 46 min east) local time
        loc = Location(mpf(35.7), angle(139, 46, 0), 24, Clock.days_from_hours(9 + 143/450))
    else:
        # Longitude 135 time zone
        loc = Location(35, 135, 0, Clock.days_from_hours(9))
    return loc

def korean_location(tee):
    """Return the location for Korean calendar; varies with moment, tee."""
    # Seoul city hall at a varying time zone.
    if (tee < GregorianDate(1908, JulianMonth.April, 1).to_fixed()):
        #local mean time for longitude 126 deg 58 min
        z = 3809/450
    elif (tee < GregorianDate(1912, JulianMonth.January, 1).to_fixed()):
        z = 8.5
    elif (tee < GregorianDate(1954, JulianMonth.March, 21).to_fixed()):
        z = 9
    elif (tee < GregorianDate(1961, JulianMonth.August, 10).to_fixed()):
        z = 8.5
    else:
        z = 9
    return Location(angle(37, 34, 0), angle(126, 58, 0), 0, Clock.days_from_hours(z))

def korean_year(cycle, year):
    """Return equivalent Korean year to Chinese cycle, cycle, and year, year."""
    return (60 * cycle) + year - 364

def vietnamese_location(tee):
    """Return the location for Vietnamese calendar is Hanoi;
    varies with moment, tee. Time zone has changed over the years."""
    if (tee < GregorianDate.new_year(1968)):
        z = 8
    else:
        z =7
    return Location(angle(21, 2, 0), angle(105, 51, 0), 12, Clock.days_from_hours(z))
