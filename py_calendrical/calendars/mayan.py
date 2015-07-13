from operator import mod
from py_calendrical.py_cal_cal import quotient, amod
from py_calendrical.calendars.julian import JD

##############################
# mayan calendars algorithms #
##############################
class MayanLongCountDate(object):

    EPOCH = JD.from_fixed(584283)
    
    def __init__(self, baktun, katun, tun, uinal, kin):
        self.baktun = baktun
        self.katun = katun
        self.tun = tun
        self.uinal = uinal
        self.kin = kin
        
    def to_fixed(self):
        """Return fixed date corresponding to the Mayan long count count,
        which is a list [baktun, katun, tun, uinal, kin]."""
        return (self.EPOCH       +
                (self.baktun * 144000) +
                (self.katun * 7200)    +
                (self.tun * 360)       +
                (self.uinal * 20)      +
                self.kin)
    
    @classmethod
    def from_fixed(cls, date):
        """Return Mayan long count date of fixed date date."""
        long_count = date - cls.EPOCH
        baktun, day_of_baktun  = divmod(long_count, 144000)
        katun, day_of_katun    = divmod(day_of_baktun, 7200)
        tun, day_of_tun        = divmod(day_of_katun, 360)
        uinal, kin             = divmod(day_of_tun, 20)
        return MayanLongCountDate(baktun, katun, tun, uinal, kin)

class MayanHaabOrdinal(object):

    def __init__(self, month, day):
        self.month = month
        self.day = day
        
    def to_ordinal(self):
        """Return the number of days into cycle of Mayan haab date h_date."""
        return ((self.month - 1) * 20) + self.day

class MayanHaabDate(MayanHaabOrdinal):

    EPOCH = MayanLongCountDate.EPOCH - MayanHaabOrdinal(18, 8).to_ordinal()
    
    def __init__(self, month, day):
        MayanHaabOrdinal.__init__(self, month, day)
    
    @classmethod
    def from_fixed(cls, date):
        """Return Mayan haab date of fixed date date."""
        count = mod(date - cls.EPOCH, 365)
        day   = mod(count, 20)
        month = quotient(count, 20) + 1
        return MayanHaabDate(month, day)
    
    def on_or_before(self, date):
        """Return fixed date of latest date on or before fixed date date
        that is Mayan haab date haab."""
        return date - mod(date - self.EPOCH - self.to_ordinal(), 365)

class MayanTzolkinOrdinal(object):

    def __init__(self, number, name):
        self.number = number
        self.name = name

    def to_ordinal(self):
        """Return number of days into Mayan tzolkin cycle of t_date."""
        return mod(self.number - 1 + (39 * (self.number - self.name)), 260)

class MayanTzolkinDate(MayanTzolkinOrdinal):

    EPOCH = MayanLongCountDate.EPOCH - MayanTzolkinOrdinal(4, 20).to_ordinal()
    
    def __init__(self, number, name):
        MayanTzolkinOrdinal.__init__(self, number, name)
    
    @classmethod
    def from_fixed(cls, date):
        """Return Mayan tzolkin date of fixed date date."""
        count  = date - cls.EPOCH + 1
        number = amod(count, 13)
        name   = amod(count, 20)
        return MayanTzolkinDate(number, name)
    
    def on_or_before(self, date):
        """Return fixed date of latest date on or before fixed date date
        that is Mayan tzolkin date tzolkin."""
        return date - mod(date - self.EPOCH - self.to_ordinal(), 260)

    @classmethod
    def mayan_year_bearer_from_fixed(cls, date):
        """Return year bearer of year containing fixed date date.
        Raises ValueError for uayeb."""
        x = MayanHaabDate(1, 0).on_or_before(date + 364)
        if MayanHaabDate.from_fixed(date).month == 19:
            raise ValueError("Invalid date")
        return cls.from_fixed(x).name

    @classmethod    
    def mayan_calendar_round_on_or_before(cls, haab, tzolkin, date):
        """Return fixed date of latest date on or before date, that is
        Mayan haab date haab and tzolkin date tzolkin.
        Raises ValueError for impossible combinations."""
        haab_count = haab.to_ordinal() + MayanHaabDate.EPOCH
        tzolkin_count = tzolkin.to_ordinal() + MayanTzolkinDate.EPOCH
        diff = tzolkin_count - haab_count
        if mod(diff, 5) == 0:
            return date - mod(date - haab_count(365 * diff), 18980)
        else:
            raise ValueError("impossible combinination")
