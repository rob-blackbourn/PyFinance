from __future__ import division
from operator import mod
from py_calendrical.py_cal_cal import amod, quotient
from py_calendrical.calendars.julian import JulianDay
from py_calendrical.calendars.gregorian import GregorianDate
from py_calendrical.utils import reduce_cond, even

class BalinesePawukonDate(object):

    EPOCH = JulianDay(146).to_fixed()
    
    def __init__(self, luang, dwiwara, triwara, caturwara, pancawara, sadwara, saptawara, asatawara, sangawara, dasawara):
        self.luang = luang
        self.dwiwara = dwiwara
        self.triwara = triwara
        self.caturwara = caturwara
        self.pancawara = pancawara
        self.sadwara = sadwara
        self.saptawara = saptawara
        self.asatawara = asatawara
        self.sangawara = sangawara
        self.dasawara = dasawara
    
    def to_tuple(self):
        return (self.luang, self.dwiwara, self.triwara, self.caturwara, self.pancawara, self.sadwara, self.saptawara, self.asatawara, self.sangawara, self.dasawara)
    
    @classmethod
    def from_fixed(cls, date):
        """Return the positions of date date in ten cycles of Balinese Pawukon
        calendar."""
        return BalinesePawukonDate(cls.luang_from_fixed(date),
                                   cls.dwiwara_from_fixed(date),
                                   cls.triwara_from_fixed(date),
                                   cls.caturwara_from_fixed(date),
                                   cls.pancawara_from_fixed(date),
                                   cls.sadwara_from_fixed(date),
                                   cls.saptawara_from_fixed(date),
                                   cls.asatawara_from_fixed(date),
                                   cls.sangawara_from_fixed(date),
                                   cls.dasawara_from_fixed(date))

    @classmethod
    def day_from_fixed(cls, date):
        """Return the position of date date in 210_day Pawukon cycle."""
        return mod(date - cls.EPOCH, 210)

    @classmethod
    def luang_from_fixed(cls, date):
        """Check membership of date date in "1_day" Balinese cycle."""
        return even(cls.dasawara_from_fixed(date))

    @classmethod
    def dwiwara_from_fixed(cls, date):
        """Return the position of date date in 2_day Balinese cycle."""
        return amod(cls.dasawara_from_fixed(date), 2)
    
    @classmethod
    def triwara_from_fixed(cls, date):
        """Return the position of date date in 3_day Balinese cycle."""
        return mod(cls.day_from_fixed(date), 3) + 1
    
    @classmethod
    def caturwara_from_fixed(cls, date):
        """Return the position of date date in 4_day Balinese cycle."""
        return amod(cls.asatawara_from_fixed(date), 4)
    
    @classmethod
    def pancawara_from_fixed(cls, date):
        """Return the position of date date in 5_day Balinese cycle."""
        return amod(cls.day_from_fixed(date) + 2, 5)
    
    @classmethod
    def sadwara_from_fixed(cls, date):
        """Return the position of date date in 6_day Balinese cycle."""
        return mod(cls.day_from_fixed(date), 6) + 1
    
    @classmethod
    def saptawara_from_fixed(cls, date):
        """Return the position of date date in Balinese week."""
        return mod(cls.day_from_fixed(date), 7) + 1
    
    @classmethod
    def asatawara_from_fixed(cls, date):
        """Return the position of date date in 8_day Balinese cycle."""
        day = cls.day_from_fixed(date)
        return mod(max(6, 4 + mod(day - 70, 210)), 8) + 1
    
    @classmethod
    def sangawara_from_fixed(cls, date):
        """Return the position of date date in 9_day Balinese cycle."""
        return mod(max(0, cls.day_from_fixed(date) - 3), 9) + 1
    
    @classmethod
    def dasawara_from_fixed(cls, date):
        """Return the position of date date in 10_day Balinese cycle."""
        i = cls.pancawara_from_fixed(date) - 1
        j = cls.saptawara_from_fixed(date) - 1
        return mod(1 + [5, 9, 7, 4, 8][i] + [5, 4, 3, 7, 8, 6, 9][j], 10)
    
    @classmethod
    def week_from_fixed(cls, date):
        """Return the  week number of date date in Balinese cycle."""
        return quotient(cls.day_from_fixed(date), 7) + 1
    
    def on_or_before(self, date):
        """Return last fixed date on or before date with Pawukon date b_date."""
        a5 = self.pancawara - 1
        a6 = self.sadwara   - 1
        b7 = self.saptawara - 1
        b35 = mod(a5 + 14 + (15 * (b7 - a5)), 35)
        days = a6 + (36 * (b35 - a6))
        cap_Delta = self.day_from_fixed(0)
        return date - mod(date + cap_Delta - days, 210)

    @classmethod    
    def positions_in_range(cls, n, c, cap_Delta, range):
        """Return the list of occurrences of n-th day of c-day cycle
        in range.
        cap_Delta is the position in cycle of RD 0."""
        a = range[0]
        b = range[1]
        pos = a + mod(n - a - cap_Delta - 1, c)
        return ([] if (pos > b) else
                [pos].extend(
                    cls.positions_in_range(n, c, cap_Delta, [pos + 1, b])))

    @classmethod    
    def kajeng_keliwon(cls, g_year):
        """Return the occurrences of Kajeng Keliwon (9th day of each
        15_day subcycle of Pawukon) in Gregorian year g_year."""
        year = GregorianDate.year_range(g_year)
        cap_Delta = cls.day_from_fixed(0)
        return cls.positions_in_range(9, 15, cap_Delta, year)
    
    @classmethod    
    def tumpek(cls, g_year):
        """Return the occurrences of Tumpek (14th day of Pawukon and every
        35th subsequent day) within Gregorian year g_year."""
        year = GregorianDate.year_range(g_year)
        cap_Delta = cls.day_from_fixed(0)
        return cls.positions_in_range(14, 35, cap_Delta, year)

    def __eq__(self, other):
        return isinstance(other, BalinesePawukonDate) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, BalinesePawukonDate) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, BalinesePawukonDate) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, BalinesePawukonDate) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, BalinesePawukonDate) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
