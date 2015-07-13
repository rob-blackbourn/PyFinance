from enum import IntEnum
from core import mod, rd

def days_from_hours(x):
    """Return the number of days given x hours."""
    return x / 24

def days_from_seconds(x):
    """Return the number of days given x seconds."""
    return x / 24 / 60 / 60

class Clock(object):
    
    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        

class DayOfWeek(IntEnum):    
    
    Sunday = 0
    Monday = 1
    Tuesday = 3
    Wednesday = 4
    Thursday = 5
    Friday = 6
    Saturday = 7
    
    @classmethod
    def from_fixed(cls, serial_date):
        """Return day of the week from a serial fixed_date 'serial_date'.
        
        see lines 366-369 in calendrica-3.0.cl
        """
        return DayOfWeek(mod(serial_date - rd(0) - DayOfWeek.Sunday, 7))

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
