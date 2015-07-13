from core import ifloor, mod

class ClockTime(object):

    def __init__(self, hours, minutes, seconds):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        
    def to_time(self):
        """Return time of day from clock time."""
        return(1/24 * (self.hours + ((self.minutes + (self.seconds / 60)) / 60)))
    
    @classmethod
    def from_time(cls, time):
        hour = ifloor(time * 24)
        minute = ifloor(mod(time * 24 * 60, 60))
        second = mod(time * 24 * 60 * 60, 60)
        return ClockTime(hour, minute, second)

    @classmethod
    def from_moment(cls, tee):
        return cls.from_time(mod(tee, 1))
    
