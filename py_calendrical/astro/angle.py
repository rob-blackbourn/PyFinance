from py_calendrical.core import ifloor, mod
from scipy.constants.constants import alpha

class DegreesMinutesSeconds(object):
    
    def __init__(self, degrees, minutes, seconds):
        self.degrees = degrees
        self.minutes = minutes
        self.seconds = seconds

    @classmethod
    def from_degrees(cls, alpha):
        """Return an angle in degrees:minutes:seconds from angle,
        'alpha' in degrees."""
        d = ifloor(alpha)
        m = ifloor(60 * mod(alpha, 1))
        s = mod(alpha * 60 * 60, 60)
        return DegreesMinutesSeconds(d, m, s)

    def to_angle(self):
        return self.degrees + ((self.minutes + (self.seconds / 60)) / 60)
