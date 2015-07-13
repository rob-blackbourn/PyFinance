from operator import mod
from py_cal_cal import quotient, amod
from py_cal_cal import JulianMonth
from py_calendrical.julian_calendars import JulianDate

AZTEC_CORRELATION = JulianDate(1521, JulianMonth.August, 13).to_fixed()

class AztecXihuitlOrdinal(object):

    def __init__(self, month, day):
        self.month = month
        self.day = day 
        
    def to_ordinal(self):
        """Return the number of elapsed days into cycle of Aztec xihuitl
        date x_date."""
        return  ((self.month - 1) * 20) + self.day - 1

class AztecXihuitlDate(AztecXihuitlOrdinal):

    CORRELATION = AZTEC_CORRELATION - AztecXihuitlOrdinal(11, 2).to_ordinal()
    
    def __init__(self, month, day):
        AztecXihuitlOrdinal.__init__(self, month, day)
        
    @classmethod
    def from_fixed(cls, date):
        """Return Aztec xihuitl date of fixed date date."""
        count = mod(date - cls.CORRELATION, 365)
        day   = mod(count, 20) + 1
        month = quotient(count, 20) + 1
        return AztecXihuitlDate(month, day)
    
    # see lines 2239-2246 in calendrica-3.0.cl
    def aztec_xihuitl_on_or_before(self, date):
        """Return fixed date of latest date on or before fixed date date
        that is Aztec xihuitl date xihuitl."""
        return (date - mod(date - self.CORRELATION - self.to_ordinal(), 365))

class AztecTonalpohuallOrdinal(object):
    
    def __init__(self, number, name):
        self.number = number
        self.name = name

    def to_ordinal(self):
        """Return the number of days into Aztec tonalpohualli cycle of t_date."""
        return mod(self.number - 1 + 39 * (self.number - self.name), 260)

class AztecTonalpohualliDate(AztecTonalpohuallOrdinal):

    CORRELATION = AZTEC_CORRELATION - AztecTonalpohuallOrdinal(1, 5).to_ordinal()
    
    def __init__(self, number, name):
        AztecTonalpohuallOrdinal.__init__(self, number, name)

    @classmethod
    def from_fixed(cls, date):
        """Return Aztec tonalpohualli date of fixed date date."""
        count  = date - cls.CORRELATION + 1
        number = amod(count, 13)
        name   = amod(count, 20)
        return AztecTonalpohualliDate(number, name)

    def on_or_before(self, date):
        """Return fixed date of latest date on or before fixed date date
        that is Aztec tonalpohualli date tonalpohualli."""
        return (date - mod(date - self.CORRELATION - self.to_ordinal(), 260))

class AztecXiuhmolpilliDesignation(AztecTonalpohualliDate):
    
    def __init__(self, number, name):
        AztecTonalpohualliDate.__init__(self, number, name)

    @classmethod    
    def from_fixed(cls, date):
        """Return designation of year containing fixed date date.
        Raises ValueError for nemontemi."""
        x = AztecXihuitlDate(18, 20).on_or_before(date + 364)
        month = AztecXihuitlDate.from_fixed(date).month
        if month == 19:
            raise ValueError("nemontemi")
        return AztecTonalpohualliDate.from_fixed(x)

    @classmethod
    def aztec_xihuitl_tonalpohualli_on_or_before(cls, xihuitl, tonalpohualli, date):
        """Return fixed date of latest xihuitl_tonalpohualli combination
        on or before date date.  That is the date on or before
        date date that is Aztec xihuitl date xihuitl and
        tonalpohualli date tonalpohualli.
        Raises ValueError for impossible combinations."""
        xihuitl_count = xihuitl.to_ordinal() + AztecXihuitlDate.CORRELATION
        tonalpohualli_count = (tonalpohualli.to_ordinal() + AztecTonalpohualliDate.CORRELATION)
        diff = tonalpohualli_count - xihuitl_count
        if mod(diff, 5) == 0:
            return date - mod(date - xihuitl_count - (365 * diff), 18980)
        else:
            raise ValueError("impossible combination")
