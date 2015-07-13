from operator import mod
from enum import IntEnum
from py_cal_cal import rd

class DayOfWeek(IntEnum):
    Sunday = 0
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6

    @classmethod
    def from_fixed(cls, date):
        """Return day of the week from a fixed date 'date'."""
        return DayOfWeek(mod(date - rd(0) - DayOfWeek.Sunday, 7))

    def on_or_before(self, fixed_date):
        """Return the fixed date of the k-day on or before fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return fixed_date - DayOfWeek.from_fixed(fixed_date - self.value)
    
    def on_or_after(self, fixed_date):
        """Return the fixed date of the k-day on or after fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 6)
    
    def nearest(self, fixed_date):
        """Return the fixed date of the k-day nearest fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 3)
    
    def after(self, fixed_date):
        """Return the fixed date of the k-day after fixed date 'fixed_date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date + 7)
    
    def before(self, fixed_date):
        """Return the fixed date of the k-day before fixed date 'date'.
        k=0 means Sunday, k=1 means Monday, and so on."""
        return self.on_or_before(fixed_date - 1)
