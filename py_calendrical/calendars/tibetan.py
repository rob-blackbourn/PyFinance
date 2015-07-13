from operator import mod
from py_calendrical.py_cal_cal import iceiling, ifloor, final_int, amod, list_range
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth

class TibetanDate(object):
    
    EPOCH = GregorianDate(-127, JulianMonth.December, 7).to_fixed()

    def __init__(self, year, month, leap_month, day, leap_day):
        self.year = year
        self.month = month
        self.leap_month = leap_month
        self.day = day
        self.leap_day = leap_day
    
    def to_fixed(self):
        """Return the fixed date corresponding to Tibetan lunar date."""
        months = ifloor((804/65 * (self.year - 1)) +
                       (67/65 * self.month) +
                       (-1 if self.leap_month else 0) +
                       64/65)
        days = (30 * months) + self.day
        mean = ((days * 11135/11312) -30 +
                (0 if self.leap_day else -1) +
                1071/1616)
        solar_anomaly = mod((days * 13/4824) + 2117/4824, 1)
        lunar_anomaly = mod((days * 3781/105840) +
                            2837/15120, 1)
        sun  = -self.sun_equation(12 * solar_anomaly)
        moon = self.moon_equation(28 * lunar_anomaly)
        return ifloor(self.EPOCH + mean + sun + moon)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Tibetan lunar date corresponding to fixed date, 'fixed_date'."""
        cap_Y = 365 + 4975/18382
        years = iceiling((fixed_date - cls.EPOCH) / cap_Y)
        year0 = final_int(years, lambda y:(fixed_date >= TibetanDate(y, 1, False, 1, False).to_fixed()))
        month0 = final_int(1, lambda m: (fixed_date >= TibetanDate(year0, m, False, 1, False).to_fixed()))
        est = fixed_date - TibetanDate(year0, month0, False, 1, False).to_fixed()
        day0 = final_int(est -2, lambda d: (fixed_date >= TibetanDate(year0, month0, False, d, False).to_fixed()))
        leap_month = (day0 > 30)
        day = amod(day0, 30)
        if (day > day0):
            temp = month0 - 1
        elif leap_month:
            temp = month0 + 1
        else:
            temp = month0
        month = amod(temp, 12)
        
        if ((day > day0) and (month0 == 1)):
            year = year0 - 1
        elif (leap_month and (month0 == 12)):
            year = year0 + 1
        else:
            year = year0
        leap_day = fixed_date == TibetanDate(year, month, leap_month, day, True).to_fixed()
        return TibetanDate(year, month, leap_month, day, leap_day)

    @classmethod        
    def sun_equation(cls, alpha):
        """Return the interpolated tabular sine of solar anomaly, 'alpha'."""
        if (alpha > 6):
            return -cls.sun_equation(alpha - 6)
        elif (alpha > 3):
            return cls.sun_equation(6 - alpha)
        elif isinstance(alpha, int):
            return [0, 6/60, 10/60, 11/60][alpha]
        else:
            return ((mod(alpha, 1) * cls.sun_equation(iceiling(alpha))) +
                    (mod(-alpha, 1) * cls.sun_equation(ifloor(alpha))))

    @classmethod
    def moon_equation(cls, alpha):
        """Return the interpolated tabular sine of lunar anomaly, 'alpha'."""
        if (alpha > 14):
            return -cls.moon_equation(alpha - 14)
        elif (alpha > 7):
            return cls.moon_equation(14 -alpha)
        elif isinstance(alpha, int):
            return [0, 5/60, 10/60, 15/60, 19/60, 22/60, 24/60, 25/60][alpha]
        else:
            return ((mod(alpha, 1) * cls.moon_equation(iceiling(alpha))) +
                    (mod(-alpha, 1) * cls.moon_equation(ifloor(alpha))))

    @classmethod
    def is_leap_month(cls, month, year):
        """Return True if 'month' is leap in Tibetan year, 'year'."""
        return month == TibetanDate.from_fixed(TibetanDate(year, month, True, 2, False).to_fixed()).month

    @classmethod
    def losar(cls, year):
        """Return the  fixed date of Tibetan New Year (Losar)
        in Tibetan year, 'year'."""
        t_leap = cls.is_leap_month(1, year)
        return TibetanDate(year, 1, t_leap, 1, False).to_fixed()

    @classmethod
    def new_year(cls, gregorian_year):
        """Return the list of fixed dates of Tibetan New Year in
        Gregorian year, 'gregorian_year'."""
        dec31  = GregorianDate.year_end(gregorian_year)
        t_year = cls.from_fixed(dec31).year
        return list_range([cls.losar(t_year - 1), cls.losar(t_year)], GregorianDate.year_range(gregorian_year))
