from enum import Enum
from py_cal_cal import amod
from py_cal_cal import JulianMonth
from py_calendrical.julian_calendars import JulianDate


class Event(Enum):
    Kalends = 1
    Nones = 2
    Ides = 3
    
class RomanDate(object):
    
    YEAR_ROME_FOUNDED = JulianDate.bce(753)

    def __init__(self, year, month, event, count, leap):
        self.year = year
        self.month = month
        self.event = event
        self.count = count
        self.leap = leap

    @classmethod
    def ides_of_month(cls, month):
        """Return the date of the Ides in Roman month 'month'."""
        return 15 if month in [JulianMonth.March, JulianMonth.May, JulianMonth.July, JulianMonth.October] else 13

    @classmethod
    def nones_of_month(cls, month):
        """Return the date of Nones in Roman month 'month'."""
        return cls.ides_of_month(month) - 8

    def to_fixed(self):
        """Return the fixed date."""
        return ({Event.Kalends: JulianDate(self.year, self.month, 1).to_fixed(),
                 Event.Nones:   JulianDate(self.year, self.month, self.nones_of_month(self.month)).to_fixed(),
                 Event.Ides:    JulianDate(self.year, self.month, self.ides_of_month(self.month)).to_fixed()
                 }[self.event] -
                self.count +
                (0 if (JulianDate.is_leap_year(self.year) and
                       (self.month == JulianMonth.March) and
                       (self.event == Event.Kalends) and
                       (16 >= self.count >= 6))
                 else 1) +
                (1 if self.leap else 0))

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Roman name corresponding to fixed fixed_date 'fixed_date'."""
        julian_date = JulianDate.from_fixed(fixed_date)
        month_prime = amod(1 + julian_date.month, 12)
        year_prime  = (julian_date.year if month_prime != 1 
                       else (julian_date.year + 1 if (julian_date.year != -1) else 1))
        kalends1 = RomanDate(year_prime, month_prime, Event.Kalends, 1, False).to_fixed()
    
        if julian_date.day == 1:
            return RomanDate(julian_date.year, julian_date.month, Event.Kalends, 1, False)
        elif julian_date.day <= cls.nones_of_month(julian_date.month):
            return RomanDate(julian_date.year,
                             julian_date.month,
                             Event.Nones, 
                             cls.nones_of_month(julian_date.month) - julian_date.day + 1,
                             False)
        elif julian_date.day <= cls.ides_of_month(julian_date.month):
            return RomanDate(julian_date.year,
                             julian_date.month,
                             Event.Ides,
                             cls.ides_of_month(julian_date.month) - julian_date.day + 1,
                             False)
        elif (julian_date.month != JulianMonth.February) or not julian_date.is_leap_year(julian_date.year):
            return RomanDate(year_prime,
                             month_prime,
                             Event.Kalends,
                             kalends1 - fixed_date + 1,
                             False)
        elif julian_date.day < 25:
            return RomanDate(julian_date.year, JulianMonth.March, Event.Kalends, 30 - julian_date.day, False)
        else:
            return RomanDate(julian_date.year, JulianMonth.March, Event.Kalends, 31 - julian_date.day, julian_date.day == 25)

    


