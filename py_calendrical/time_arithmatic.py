from operator import mod
from py_cal_cal import ifloor

class Clock(object):
    
    def __init__(self, hour, minute, second):
        self.hour = hour
        self.minute = minute
        self.second = second

    def to_time(self):
        """Return time of day from clock time 'hms'."""
        return(1/24 * (self.hour + ((self.minute + (self.second / 60)) / 60)))

    @classmethod
    def from_moment(cls, tee):
        """Return clock time hour:minute:second from moment 'tee'."""
        time = cls.time_from_moment(tee)
        hour = ifloor(time * 24)
        minute = ifloor(mod(time * 24 * 60, 60))
        second = mod(time * 24 * 60 * 60, 60)
        return Clock(hour, minute, second)

    @classmethod
    def fixed_from_moment(cls, tee):
        """Return fixed date from moment 'tee'."""
        return ifloor(tee)
    
    @classmethod
    def time_from_moment(cls, tee):
        """Return time from moment 'tee'."""
        return mod(tee, 1)

    @classmethod
    def days_from_hours(cls, hours):
        """Return the number of days given x hours."""
        return hours / 24
    
    @classmethod
    def days_from_seconds(cls, seconds):
        """Return the number of days given x seconds."""
        return seconds / 24 / 60 / 60
