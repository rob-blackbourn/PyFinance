from gregorian_calendars import JulianMonth 
from py_calendrical.julian_calendars import JulianDate
from coptic_calendars import CopticDate

class EthiopicDate(object):
    
    EPOCH = JulianDate(JulianDate.ce(8), JulianMonth.August, 29).to_fixed()

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def to_fixed(self):
        """Return the fixed date corresponding to Ethiopic date 'e_date'."""
        return (self.EPOCH + CopticDate(self.year, self.month, self.day).to_fixed() - CopticDate.EPOCH)

    @classmethod
    def from_fixed(cls, date):
        """Return the Ethiopic date equivalent of fixed date 'date'."""
        ymd = CopticDate.from_fixed(date + (CopticDate.EPOCH - cls.EPOCH))
        return EthiopicDate(ymd.year, ymd.month, ymd.day)
