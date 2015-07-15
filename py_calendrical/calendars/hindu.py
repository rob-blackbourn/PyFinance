from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.py_cal_cal import amod, quotient, iceiling, ifloor, iround, signum, binary_search
from py_calendrical.py_cal_cal import invert_angular
from py_calendrical.triganometry import angle, sin_degrees
from py_calendrical.day_arithmatic import DayOfWeek
from py_calendrical.calendars.julian import JulianDate
from py_calendrical.location import Location
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.time_arithmatic import Clock
from py_calendrical.utils import reduce_cond, next_int, is_in_range, list_range
from py_calendrical.solar import Solar
from py_calendrical.astro import Astro
from py_calendrical.lunar import Lunar


class OldHindu(object):
    
    ARYA_SOLAR_YEAR = 1577917500/4320000
    ARYA_SOLAR_MONTH = ARYA_SOLAR_YEAR / 12

    EPOCH = JulianDate(JulianDate.bce(3102), JulianMonth.February, 18).to_fixed()
    ARYA_JOVIAN_PERIOD =  1577917500/364224

    @classmethod    
    def hindu_day_count(cls, date):
        """Return elapsed days (Ahargana) to date date since Hindu epoch (KY)."""
        return date - cls.EPOCH

    @classmethod
    def jovian_year(cls, date):
        """Return year of Jupiter cycle at fixed date date."""
        return amod(quotient(cls.hindu_day_count(date), cls.ARYA_JOVIAN_PERIOD / 12) + 27, 60)

class OldHinduLunarDate(OldHindu):
    
    ARYA_LUNAR_MONTH = 1577917500/53433336
    ARYA_LUNAR_DAY =  ARYA_LUNAR_MONTH / 30

    def __init__(self, year, month, leap, day):
        self.year = year
        self.month = month
        self.leap = leap
        self.day = day
        
    def to_fixed(self):
        """Return fixed date corresponding to Old Hindu lunar date l_date."""
        mina  = ((12 * self.year) - 1) * self.ARYA_SOLAR_MONTH
        lunar_new_year = self.ARYA_LUNAR_MONTH * (quotient(mina, self.ARYA_LUNAR_MONTH) + 1)
    
        if not self.leap and iceiling((lunar_new_year - mina) / (self.ARYA_SOLAR_MONTH - self.ARYA_LUNAR_MONTH)) <= self.month:
            temp = self.month
        else:
            temp = self.month - 1
            
        temp = self.EPOCH + lunar_new_year + (self.ARYA_LUNAR_MONTH * temp) + ((self.day - 1) * self.ARYA_LUNAR_DAY) + Clock.days_from_hours(-6)
        
        return iceiling(temp)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return Old Hindu lunar date equivalent to fixed date 'fixed_date'."""
        sun = cls.hindu_day_count(fixed_date) + Clock.days_from_hours(6)
        new_moon = sun - mod(sun, cls.ARYA_LUNAR_MONTH)
        leap = cls.ARYA_SOLAR_MONTH - cls.ARYA_LUNAR_MONTH >= mod(new_moon, cls.ARYA_SOLAR_MONTH) and mod(new_moon, cls.ARYA_SOLAR_MONTH) > 0
        month = mod(iceiling(new_moon / cls.ARYA_SOLAR_MONTH), 12) + 1
        day = mod(quotient(sun, cls.ARYA_LUNAR_DAY), 30) + 1
        year = iceiling((new_moon + cls.ARYA_SOLAR_MONTH) / cls.ARYA_SOLAR_YEAR) - 1
        return OldHinduLunarDate(year, month, leap, day)

    @classmethod
    def is_leap_year(cls, year):
        """Return True if year is a leap year on the
        old Hindu calendar."""
        return mod(year * cls.ARYA_SOLAR_YEAR - cls.ARYA_SOLAR_MONTH, cls.ARYA_LUNAR_MONTH) >= 23902504679/1282400064

    def to_tuple(self):
        return (self.year, self.month, self.leap, self.day)
    
    def __eq__(self, other):
        return isinstance(other, OldHinduLunarDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, OldHinduLunarDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, OldHinduLunarDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, OldHinduLunarDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, OldHinduLunarDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)

class OldHinduSolarDate(OldHindu):
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_fixed(cls, date):
        """Return Old Hindu solar date equivalent to fixed date date."""
        sun   = cls.hindu_day_count(date) + Clock.days_from_hours(6)
        year  = quotient(sun, cls.ARYA_SOLAR_YEAR)
        month = mod(quotient(sun, cls.ARYA_SOLAR_MONTH), 12) + 1
        day   = ifloor(mod(sun, cls.ARYA_SOLAR_MONTH)) + 1
        return OldHinduSolarDate(year, month, day)
        
    def to_fixed(self):
        """Return fixed date corresponding to Old Hindu solar date s_date."""
        return iceiling(self.EPOCH + self.year * self.ARYA_SOLAR_YEAR + (self.month - 1) * self.ARYA_SOLAR_MONTH + self.day + Clock.days_from_hours(-30))

    def to_tuple(self):
        return (self.year, self.month, self.day)

    def __eq__(self, other):
        return isinstance(other, OldHinduSolarDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, OldHinduSolarDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, OldHinduSolarDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, OldHinduSolarDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, OldHinduSolarDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
class HinduDate(object):

    SIDEREAL_YEAR = 365 + 279457/1080000
    ANOMALISTIC_YEAR = 1577917828000/(4320000000 - 387)
    CREATION = OldHindu.EPOCH - 1955880000 * SIDEREAL_YEAR
    UJJAIN = Location(angle(23, 9, 0), angle(75, 46, 6), 0, Clock.days_from_hours(5 + 461/9000))
    LOCATION = UJJAIN

    def __init__(self, year, month, leap_month, day, leap_day):
        self.year = year
        self.month = month
        self.leap_month = leap_month
        self.day = day
        self.leap_day = leap_day

    def to_tuple(self):
        return (self.year, self.month, self.leap_month, self.day, self.leap_day)

    def __eq__(self, other):
        return isinstance(other, HinduDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, HinduDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, HinduDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, HinduDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, HinduDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    @classmethod
    def sine_table(cls, entry):
        """Return the value for entry in the Hindu sine table.
        Entry, entry, is an angle given as a multiplier of 225'."""
        exact = 3438 * sin_degrees(entry * angle(0, 225, 0))
        error = 0.215 * signum(exact) * signum(abs(exact) - 1716)
        return iround(exact + error) / 3438

    @classmethod
    def sine(cls, theta):
        """Return the linear interpolation for angle, theta, in Hindu table."""
        entry    = theta / angle(0, 225, 0)
        fraction = mod(entry, 1)
        return ((fraction * cls.sine_table(iceiling(entry))) + ((1 - fraction) * cls.sine_table(ifloor(entry))))

    @classmethod
    def arcsin(cls, amp):
        """Return the inverse of Hindu sine function of amp."""
        if (amp < 0):
            return -cls.arcsin(-amp)
        else:
            pos = next_int(0, lambda k: amp <= cls.sine_table(k))
            below = cls.sine_table(pos - 1)
            return (angle(0, 225, 0) * (pos - 1 + ((amp - below) / (cls.sine_table(pos) - below))))

    @classmethod
    def mean_position(cls, tee, period):
        """Return the position in degrees at moment, tee, in uniform circular
        orbit of period days."""
        return 360 * mod((tee - cls.CREATION) / period, 1)

    @classmethod
    def true_position(cls, tee, period, size, anomalistic, change):
        """Return the longitudinal position at moment, tee.
        period is the period of mean motion in days.
        size is ratio of radii of epicycle and deferent.
        anomalistic is the period of retrograde revolution about epicycle.
        change is maximum decrease in epicycle size."""
        lam         = cls.mean_position(tee, period)
        offset      = cls.sine(cls.mean_position(tee, anomalistic))
        contraction = abs(offset) * change * size
        equation    = cls.arcsin(offset * (size - contraction))
        return mod(lam - equation, 360)

    @classmethod
    def solar_longitude(cls, tee):
        """Return the solar longitude at moment, tee."""
        return cls.true_position(tee, cls.SIDEREAL_YEAR, 14/360, cls.ANOMALISTIC_YEAR, 1/42)

    @classmethod
    def zodiac(cls, tee):
        """Return the zodiacal sign of the sun, as integer in range 1..12,
        at moment tee."""
        return quotient(float(cls.solar_longitude(tee)), 30) + 1

    @classmethod
    def equation_of_time(cls, date):
        """Return the time from true to mean midnight of date, date."""
        offset = cls.sine(cls.mean_position(date, cls.ANOMALISTIC_YEAR))
        equation_sun = (offset * angle(57, 18, 0) * (14/360 - (abs(offset) / 1080)))
        return ((cls.daily_motion(date) / 360) * (equation_sun / 360) * cls.SIDEREAL_YEAR)

    @classmethod
    def ascensional_difference(cls, date, location):
        """Return the difference between right and oblique ascension
        of sun on date, date, at loacel, location."""
        sin_delta = (1397/3438) * cls.sine(cls.tropical_longitude(date))
        phi = location.latitude
        diurnal_radius = cls.sine(90 + cls.arcsin(sin_delta))
        tan_phi = cls.sine(phi) / cls.sine(90 + phi)
        earth_sine = sin_delta * tan_phi
        return cls.arcsin(-earth_sine / diurnal_radius)

    @classmethod
    def daily_motion(cls, date):
        """Return the sidereal daily motion of sun on date, date."""
        mean_motion = 360 / cls.SIDEREAL_YEAR
        anomaly = cls.mean_position(date, cls.ANOMALISTIC_YEAR)
        epicycle = 14/360 - abs(cls.sine(anomaly)) / 1080
        entry = quotient(float(anomaly), angle(0, 225, 0))
        sine_table_step = cls.sine_table(entry + 1) - cls.sine_table(entry)
        factor = -3438/225 * sine_table_step * epicycle
        return mean_motion * (factor + 1)

    @classmethod
    def solar_sidereal_difference(cls, date):
        """Return the difference between solar and sidereal day on date, date."""
        return cls.daily_motion(date) * cls.rising_sign(date)

    @classmethod
    def sunrise(cls, date):
        """Return the sunrise at hindu_location on date, date."""
        return (date + Clock.days_from_hours(6) + 
                ((cls.UJJAIN.longitude - cls.LOCATION.longitude) / 360) -
                cls.equation_of_time(date) +
                ((1577917828/1582237828 / 360) *
                 (cls.ascensional_difference(date, cls.LOCATION) +
                  (1/4 * cls.solar_sidereal_difference(date)))))

    @classmethod
    def sunset(cls, date):
        """Return sunset at HINDU_LOCATION on date, date."""
        return (date + Clock.days_from_hours(18) + 
                ((cls.UJJAIN.longitude - cls.LOCATION.longitude) / 360) -
                cls.equation_of_time(date) +
                (((1577917828/1582237828) / 360) *
                 (- cls.ascensional_difference(date, cls.LOCATION) +
                  (3/4 * cls.solar_sidereal_difference(date)))))

    @classmethod
    def alt_sunrise(cls, date):
        """Return the astronomical sunrise at Hindu location on date, date,
        per Lahiri, rounded to nearest minute, as a rational number."""
        rise = cls.UJJAIN.dawn(date, angle(0, 47, 0))
        return 1/24 * 1/60 * iround(rise * 24 * 60)

class HinduLunarDate(HinduDate):

    MONTH = 27 + 4644439/14438334
    SYNODIC_MONTH = 29 + 7087771/13358334
    ANOMALISTIC_MONTH = mpf(1577917828)/(57753336 - 488199)
    LUNAR_ERA = 3044

    def __init__(self, year, month, leap_month, day, leap_day):
        HinduDate.__init__(self, year, month, leap_month, day, leap_day)
        
    @classmethod
    def from_fixed(cls, date):
        """Return the Hindu lunar date, new_moon scheme, 
        equivalent to fixed date, date."""
        critical = cls.sunrise(date)
        day = cls.lunar_day_from_moment(critical)
        leap_day = (day == cls.lunar_day_from_moment(cls.sunrise(date - 1)))
        last_new_moon = cls.new_moon_before(critical)
        next_new_moon = cls.new_moon_before(ifloor(last_new_moon) + 35)
        solar_month = cls.zodiac(last_new_moon)
        leap_month = (solar_month == cls.zodiac(next_new_moon))
        month = amod(solar_month + 1, 12)
        year = cls.calendar_year((date + 180) if (month <= 2) else date) - cls.LUNAR_ERA
        return HinduLunarDate(year, month, leap_month, day, leap_day)

    def to_fixed(self):
        """Return the fixed date of this Hindu lunar date."""
        approx = OldHindu.EPOCH + (self.SIDEREAL_YEAR * (self.year + self.LUNAR_ERA + ((self.month - 1) / 12)))
        s = ifloor(approx - ((1/360) * self.SIDEREAL_YEAR * mod(self.hindu_solar_longitude(approx) - ((self.month - 1) * 30) + 180, 360) - 180))
        k = self.lunar_day_from_moment(s + Clock.days_from_hours(6))
        if (3 < k < 27):
            temp = k
        else:
            mid = self.lunar_from_fixed(s - 15)
            if ((mid.month != self.month) or
                (mid.leap_month and not self.leap_month)):
                temp = mod(k + 15, 30) - 15
            else:
                temp = mod(k - 15, 30) + 15
        est = s + self.day - temp
        tau = est - mod(self.lunar_day_from_moment(est + Clock.days_from_hours(6)) - self.day + 15, 30) + 15
        date = next_int(tau - 1, lambda d: self.lunar_day_from_moment(self.sunrise(d)) in [self.day, amod(self.day + 1, 30)])
        return date + 1 if self.leap_day else date

    @classmethod
    def lunar_longitude(cls, tee):
        """Return the lunar longitude at moment, tee."""
        return cls.true_position(tee, cls.SIDEREAL_MONTH, 32/360, cls.ANOMALISTIC_MONTH, 1/96)

    @classmethod
    def lunar_phase(cls, tee):
        """Return the longitudinal distance between the sun and moon
        at moment, tee."""
        return mod(cls.lunar_longitude(tee) - cls.hindu_solar_longitude(tee), 360)

    @classmethod
    def lunar_day_from_moment(cls, tee):
        """Return the phase of moon (tithi) at moment, tee, as an integer in
        the range 1..30."""
        return quotient(cls.lunar_phase(tee), 12) + 1

    @classmethod
    def new_moon_before(cls, tee):
        """Return the approximate moment of last new moon preceding moment, tee,
        close enough to determine zodiacal sign."""
        varepsilon = pow(2, -1000)
        tau = tee - ((1/360) * cls.lunar_phase(tee) * cls.SYNODIC_MONTH)
        return binary_search(tau - 1, min(tee, tau + 1),
                             lambda l, u: cls.zodiac(l) == cls.zodiac(u) or u - l < varepsilon,
                             lambda x: cls.lunar_phase(x) < 180)

    @classmethod
    def lunar_day_at_or_after(cls, k, tee):
        """Return the time lunar_day (tithi) number, k, begins at or after
        moment, tee.  k can be fractional (for karanas)."""
        phase = (k - 1) * 12
        tau   = tee + ((1/360) * mod(phase - cls.lunar_phase(tee), 360) * cls.SYNODIC_MONTH)
        a = max(tee, tau - 2)
        b = tau + 2
        return invert_angular(cls.lunar_phase, phase, a, b)

    @classmethod
    def calendar_year(cls, tee):
        """Return the solar year at given moment, tee."""
        return iround(((tee - OldHindu.EPOCH) / cls.SIDEREAL_YEAR) - (cls.solar_longitude(tee) / 360))

class HinduLunarFullMoonDate(HinduDate):
    
    def __init__(self, year, month, leap_month, day, leap_day):
        HinduDate.__init__(self, year, month, leap_month, day, leap_day)

    def to_fixed(self):
        """Return the fixed date equivalent to Hindu lunar date, l_date,
        in full_moon scheme."""
        if self.leap_month or self.day <= 15:
            m = self.month
        elif self.is_expunged(amod(self.month - 1, 12), self.year):
            m = amod(self.month - 2, 12)
        else:
            m = amod(self.month - 1, 12)
        return HinduLunarFullMoonDate(self.year, m, self.leap_month, self.day, self.leap_day).to_fixed()

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Hindu lunar date, full_moon scheme, 
        equivalent to fixed date, 'fixed_date'."""
        l_date     = cls.from_fixed(fixed_date)
        m = cls.from_fixed(fixed_date + 20).month if l_date.day >= 16 else l_date.month
        return HinduLunarFullMoonDate(l_date.year, m, l_date.leap_month, l_date.day, l_date.leap_day)
    
    @classmethod
    def is_expunged(cls, month, year):
        """Return True if Hindu lunar month 'month' in year, 'year' is expunged."""
        return month != cls.lunar_from_fixed(HinduLunarFullMoonDate(year, month, False, 15, False).to_fixed()).month
    
    
class HinduSolarDate(HinduDate):
    
    SOLAR_ERA = 3179
    
    def __init__(self, year, month, leap_month, day, leap_day):
        HinduDate.__init__(self, year, month, leap_month, day, leap_day)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Hindu (Orissa) solar date equivalent to fixed date, 'fixed_date'."""
        critical = cls.sunrise(fixed_date + 1)
        month    = cls.zodiac(critical)
        year     = cls.calendar_year(critical) - cls.SOLAR_ERA
        approx   = fixed_date - 3 - mod(ifloor(cls.solar_longitude(critical)), 30)
        begin    = next_int(approx, lambda i: (cls.zodiac(cls.sunrise(i + 1)) ==  month))
        day      = fixed_date - begin + 1
        return HinduSolarDate(year, month, day)

    def to_fixed(self):
        """Return the fixed date corresponding to Hindu solar date, s_date,
        (Saka era; Orissa rule.)"""
        begin = ifloor((self.year + self.SOLAR_ERA + ((self.month - 1)/12)) * self.SIDEREAL_YEAR + OldHindu.EPOCH)
        return self.day - 1 + next_int(begin - 3, lambda d: self.zodiac(self.sunrise(d + 1)) == self.month)

    @classmethod
    def tropical_longitude(cls, fixed_date):
        """Return the Hindu tropical longitude on fixed date, 'fixed_date'.
        Assumes precession with maximum of 27 degrees
        and period of 7200 sidereal years (= 1577917828/600 days)."""
        days = ifloor(fixed_date - OldHindu.EPOCH)
        precession = 27 - abs(54 - mod(27 + (108 * 600/1577917828 * days), 108))
        return mod(cls.solar_longitude(fixed_date) - precession, 360)

    @classmethod
    def rising_sign(cls, fixed_date):
        """Return the tabulated speed of rising of current zodiacal sign on date, date."""
        i = quotient(float(cls.tropical_longitude(fixed_date)), 30)
        return [1670/1800, 1795/1800, 1935/1800, 1935/1800, 1795/1800, 1670/1800][mod(i, 6)]

    @classmethod
    def sundial_time(cls, tee):
        """Return Hindu local time of temporal moment, tee."""
        date = Clock.fixed_from_moment(tee)
        time = mod(tee, 1)
        q    = ifloor(4 * time)
        if q == 0:
            a = cls.sunset(date - 1)
            b = cls.sunrise(date)
            t = Clock.days_from_hours(-6)
        elif q == 3:
            a = cls.sunset(date)
            b = cls.sunrise(date + 1)
            t = Clock.days_from_hours(18)
        else:
            a = cls.sunrise(date)
            b = cls.sunset(date)
            t = Clock.days_from_hours(6)
        return a + (2 * (b - a) * (time - t))

def ayanamsha(tee):
    """Return the difference between tropical and sidereal solar longitude."""
    return Solar.solar_longitude(tee) - sidereal_solar_longitude(tee)

class HinduAstro(HinduDate):
    
    MEAN_SIDEREAL_YEAR = mpf(365.25636)
    
    def __init__(self, year, month, leap_month, day, leap_day):
        HinduDate.__init__(self, year, month, leap_month, day, leap_day)

    @classmethod
    def sunset(cls, date):
        """Return the geometrical sunset at Hindu location on date, date."""
        return cls.UJJAIN.dusk(date, 0)

    @classmethod
    def calendar_year(cls, tee):
        """Return the astronomical Hindu solar year KY at given moment, tee."""
        return iround(((tee - OldHindu.EPOCH) / cls.MEAN_SIDEREAL_YEAR) - (sidereal_solar_longitude(tee) / 360))

def sidereal_zodiac(tee):
    """Return the sidereal zodiacal sign of the sun, as integer in range
    1..12, at moment, tee."""
    return quotient(int(sidereal_solar_longitude(tee)), 30) + 1

class HinduAstroSolar(HinduAstro):
    
    def __init__(self, year, month, leap_month, day, leap_day):
        HinduAstro.__init__(self, year, month, leap_month, day, leap_day)

    def to_fixed(self):
        """Return the fixed date corresponding to Astronomical 
        Hindu solar date (Tamil rule; Saka era)."""
        approx = OldHindu.EPOCH - 3 + ifloor(((self.year + HinduSolarDate.SOLAR_ERA) + ((self.month - 1) / 12)) * self.MEAN_SIDEREAL_YEAR)
        begin = next_int(approx, lambda i: sidereal_zodiac(self.sunset(i)) == self.month)
        return begin + self.day - 1

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Astronomical Hindu (Tamil) solar date equivalent to
        fixed date, 'fixed_date'."""
        critical = cls.sunset(fixed_date)
        month    = sidereal_zodiac(critical)
        year     = cls.calendar_year(critical) - HinduSolarDate.SOLAR_ERA
        approx   = fixed_date - 3 - mod(ifloor(sidereal_solar_longitude( critical)), 30)
        begin    = next_int(approx, lambda i: (sidereal_zodiac(cls.sunset(i)) == month))
        day      = fixed_date - begin + 1
        return HinduAstroSolar(year, month, day)

class HinduAstroLunar(HinduAstro):
    
    def __init__(self, year, month, leap_month, day, leap_day):
        HinduAstro.__init__(self, year, month, leap_month, day, leap_day)
        
    @classmethod
    def day_from_moment(cls, tee):
        """Return the phase of moon (tithi) at moment, tee, as an integer in
        the range 1..30."""
        return quotient(cls.lunar_phase(tee), 12) + 1

    @classmethod
    def from_fixed(cls, date):
        """Return the astronomical Hindu lunar date equivalent to
        fixed date, date."""
        critical = cls.alt_sunrise(date)
        day      = cls.day_from_moment(critical)
        leap_day = (day == cls.day_from_moment(cls.alt_sunrise(date - 1)))
        last_new_moon = cls.new_moon_before(critical)
        next_new_moon = cls.new_moon_at_or_after(critical)
        solar_month   = sidereal_zodiac(last_new_moon)
        leap_month    = solar_month == sidereal_zodiac(next_new_moon)
        month    = amod(solar_month + 1, 12)
        year     = cls.calendar_year((date + 180)
                                             if (month <= 2)
                                             else date) - cls.LUNAR_ERA
        return HinduAstroLunar(year, month, leap_month, day, leap_day)

    def to_fixed(self):
        """Return the fixed date corresponding to Hindu lunar date, l_date."""
        approx = (OldHindu.EPOCH + self.MEAN_SIDEREAL_YEAR * (self.year + self.LUNAR_ERA + ((self.month - 1) / 12)))
        s = ifloor(approx -
                  1/360 * self.MEAN_SIDEREAL_YEAR *
                  (mod(sidereal_solar_longitude(approx) -
                      (self.month - 1) * 30 + 180, 360) - 180))
        k = self.day_from_moment(s + Clock.days_from_hours(6))
        if (3 < k < 27):
            temp = k
        else:
            mid = self.from_fixed(s - 15)
            if ((mid.month != self.month) or (mid.leap_month and not self.leap_month)):
                temp = mod(k + 15, 30) - 15
            else:
                temp = mod(k - 15, 30) + 15
        est = s + self.day - temp
        tau = est - mod(self.day_from_moment(est + Clock.days_from_hours(6)) - self.day + 15, 30) + 15
        date = next_int(tau - 1,
                    lambda d: (self.day_from_moment(self.alt_sunrise(d)) in
                               [self.day, amod(self.day + 1, 30)]))
        return (date + 1) if self.leap_day else date

def hindu_lunar_station(date):
    """Return the Hindu lunar station (nakshatra) at sunrise on date, date."""
    critical = HinduDate.sunrise(date)
    return quotient(HinduLunarDate.longitude(critical), angle(0, 800, 0)) + 1

def hindu_solar_longitude_at_or_after(lam, tee):
    """Return the moment of the first time at or after moment, tee
    when Hindu solar longitude will be lam degrees."""
    tau = tee + (HinduSolarDate.SIDEREAL_YEAR * (1 / 360) * mod(lam - HinduDate.solar_longitude(tee), 360))
    a = max(tee, tau - 5)
    b = tau +5
    return invert_angular(HinduDate.solar_longitude, lam, a, b)

def mesha_samkranti(g_year):
    """Return the fixed moment of Mesha samkranti (Vernal equinox)
    in Gregorian year, g_year."""
    jan1 = GregorianDate.new_year(g_year)
    return hindu_solar_longitude_at_or_after(0, jan1)


# see lines 5495-5513 in calendrica-3.0.cl
def hindu_lunar_new_year(g_year):
    """Return the fixed date of Hindu lunisolar new year in
    Gregorian year, g_year."""
    jan1     = GregorianDate.new_year(g_year)
    mina     = hindu_solar_longitude_at_or_after(330, jan1)
    new_moon = HinduLunarDate.day_at_or_after(1, mina)
    h_day    = ifloor(new_moon)
    critical = HinduDate.sunrise(h_day)
    return (h_day +
            (0 if ((new_moon < critical) or
                   (HinduLunarDate.day_from_moment(HinduDate.sunrise(h_day + 1)) == 2))
             else 1))


# see lines 5515-5539 in calendrica-3.0.cl
def is_hindu_lunar_on_or_before(l_date1, l_date2):
    """Return True if Hindu lunar date, l_date1 is on or before
    Hindu lunar date, l_date2."""
    return ((l_date1.year < l_date2.year) or
            ((l_date1.year == l_date2.year) and
             ((l_date1.month < l_date2.month) or
              ((l_date1.month == l_date2.month) and
               ((l_date1.leap_month and not l_date2.leap_month) or
                ((l_date1.leap_month == l_date2.leap_month) and
                 ((l_date1.day < l_date2.day) or
                  ((l_date1.day == l_date2.day) and
                   ((not l_date1.leap_day) or
                    l_date2.leap_day)))))))))


# see lines 5941-5967 in calendrica-3.0.cl
def hindu_date_occur(l_month, l_day, l_year):
    """Return the fixed date of occurrence of Hindu lunar month, l_month,
    day, l_day, in Hindu lunar year, l_year, taking leap and
    expunged days into account.  When the month is
    expunged, then the following month is used."""
    lunar = HinduLunarDate(l_year, l_month, False, l_day, False)
    ttry   = lunar.to_fixed()
    mid   = HinduLunarDate.from_fixed((ttry - 5) if (l_day > 15) else ttry)
    expunged = l_month != mid.month
    l_date = HinduLunarDate(mid.year, mid.month, mid.leap_month, l_day, False)
    if (expunged):
        return next_int(ttry,
                    lambda d: (not is_hindu_lunar_on_or_before(
                        HinduLunarDate.from_fixed(d),
                        l_date))) - 1
    elif (l_day != HinduLunarDate.from_fixed(ttry).day):
        return ttry - 1
    else:
        return ttry

def hindu_lunar_holiday(l_month, l_day, gregorian_year):
    """Return the list of fixed dates of occurrences of Hindu lunar
    month, month, day, day, in Gregorian year, 'gregorian_year'."""
    l_year = HinduLunarDate.from_fixed(GregorianDate.new_year(gregorian_year)).year
    date1  = hindu_date_occur(l_month, l_day, l_year)
    date2  = hindu_date_occur(l_month, l_day, l_year + 1)
    return list_range([date1, date2], GregorianDate.year_range(gregorian_year))

def diwali(gregorian_year):
    """Return the list of fixed date(s) of Diwali in Gregorian year, 'gregorian_year'."""
    return hindu_lunar_holiday(8, 1, gregorian_year)

def hindu_tithi_occur(l_month, tithi, tee, l_year):
    """Return the fixed date of occurrence of Hindu lunar tithi prior
    to sundial time, tee, in Hindu lunar month, l_month, and
    year, l_year."""
    approx = hindu_date_occur(l_month, ifloor(tithi), l_year)
    lunar  = HinduLunarDate.day_at_or_after(tithi, approx - 2)
    ttry    = Clock.fixed_from_moment(lunar)
    tee_h  = HinduLunarDate.UJJAIN.standard_from_sundial(ttry + tee)
    if lunar <= tee_h or HinduLunarDate.lunar_phase(HinduLunarDate.UJJAIN.standard_from_sundial(ttry + 1 + tee)) > 12 * tithi:
        return ttry
    else:
        return ttry + 1

def hindu_lunar_event(l_month, tithi, tee, gregorian_year):
    """Return the list of fixed dates of occurrences of Hindu lunar tithi
    prior to sundial time, tee, in Hindu lunar month, l_month,
    in Gregorian year, 'gregorian_year'."""
    l_year = HinduLunarDate.from_fixed(GregorianDate.new_year(gregorian_year)).year
    date1  = hindu_tithi_occur(l_month, tithi, tee, l_year)
    date2  = hindu_tithi_occur(l_month, tithi, tee, l_year + 1)
    return list_range([date1, date2], GregorianDate.year_range(gregorian_year))

def shiva(gregorian_year):
    """Return the list of fixed date(s) of Night of Shiva in Gregorian year, 'gregorian_year'."""
    return hindu_lunar_event(11, 29, Clock.days_from_hours(24), gregorian_year)

def rama(gregorian_year):
    """Return the list of fixed date(s) of Rama's Birthday in Gregorian
    year, 'gregorian_year'."""
    return hindu_lunar_event(1, 9, Clock.days_from_hours(12), gregorian_year)

def karana(n):
    """Return the number (0-10) of the name of the n-th (1-60) Hindu karana."""
    if n == 1:
        return 0
    elif n > 57:
        return n - 50
    else:
        return amod(n - 1, 7)

def yoga(date):
    """Return the Hindu yoga on date, date."""
    return ifloor(mod((HinduSolarDate.longitude(date) + HinduLunarDate.longitude(date)) / angle(0, 800, 0), 27)) + 1

def sacred_wednesdays(g_year):
    """Return the list of Wednesdays in Gregorian year, g_year,
    that are day 8 of Hindu lunar months."""
    return sacred_wednesdays_in_range(GregorianDate.year_range(g_year))

def sacred_wednesdays_in_range(range):
    """Return the list of Wednesdays within range of dates
    that are day 8 of Hindu lunar months."""
    a      = range[0]
    b      = range[1]
    wed    = DayOfWeek.Wednesday.on_or_after(a)
    h_date = HinduLunarDate.from_fixed(wed)
    ell  = [wed] if (h_date.day == 8) else []
    if is_in_range(wed, range):
        ell[:0] = sacred_wednesdays_in_range([wed + 1, b])
        return ell
    else:
        return []

SIDEREAL_START = Astro.precession(HinduDate.UJJAIN.universal_from_local(mesha_samkranti(JulianDate.ce(285))))

def sidereal_solar_longitude(tee):
    """Return sidereal solar longitude at moment, tee."""
    return mod(Solar.solar_longitude(tee) - Astro.precession(tee) + SIDEREAL_START, 360)

def sidereal_lunar_longitude(tee):
    """Return sidereal lunar longitude at moment, tee."""
    return mod(Lunar.lunar_longitude(tee) - Astro.precession(tee) + SIDEREAL_START, 360)
