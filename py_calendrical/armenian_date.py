from core import rd
from egyptian_date import EgyptianDate

class ArmenianDate(object):

    EPOCH = rd(201443)
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_fixed(self):
        """Return the fixed date."""
        return (self.EPOCH +
                EgyptianDate(self.year, self.month, self.day).to_fixed() -
                EgyptianDate.EPOCH)

    @classmethod
    def from_fixed(cls, fixed_date):
        """Return the Armenian fixed_date corresponding to fixed fixed_date 'fixed_date'."""
        ymd = EgyptianDate.from_fixed(fixed_date + (EgyptianDate.EPOCH - cls.EPOCH))
        return ArmenianDate(ymd.year, ymd.month, ymd.day)
