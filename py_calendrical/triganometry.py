from __future__ import division
from operator import mod
from py_cal_cal import signum, ifloor
from mpmath import radians as radians_from_degrees, degrees, sin, cos, tan, mpf, atan, asin, acos

def secs(x):
    """Return the seconds in angle x."""
    return x / 3600.0

def angle(d, m, s):
    """Return an angle data structure
    from d degrees, m arcminutes and s arcseconds.
    This assumes that negative angles specifies negative d, m and s."""
    return d + ((m + (s / 60)) / 60)

def normalized_degrees(theta):
    """Return a normalize angle theta to range [0,360) degrees."""
    return mod(theta, 360)

def normalized_degrees_from_radians(theta):
    """Return normalized degrees from radians, theta.
    Function 'degrees' comes from mpmath."""
    return normalized_degrees(degrees(theta))

def sin_degrees(theta):
    """Return sine of theta (given in degrees)."""
    return sin(radians_from_degrees(theta))

def cos_degrees(theta):
    """Return cosine of theta (given in degrees)."""
    return cos(radians_from_degrees(theta))

def tan_degrees(theta):
    """Return tangent of theta (given in degrees)."""
    return tan(radians_from_degrees(theta))

#-----------------------------------------------------------
# NOTE: arc[tan|sin|cos] casted with degrees given CL code
#       returns angles [0, 360), see email from Dershowitz
#       after my request for clarification
#-----------------------------------------------------------

# see lines 2728-2739 in calendrica-3.0.cl
# def arctan_degrees(y, x):
#     """ Arctangent of y/x in degrees."""
#     from math import atan2
#     return normalized_degrees_from_radians(atan2(x, y))

def arctan_degrees(y, x):
    """ Arctangent of y/x in degrees."""
    if x == 0 and y != 0:
        return mod(signum(y) * mpf(90), 360)
    else:
        alpha = normalized_degrees_from_radians(atan(y / x))
        if x >= 0:
            return alpha
        else:
            return mod(alpha + mpf(180), 360)

def arcsin_degrees(x):
    """Return arcsine of x in degrees."""
    return normalized_degrees_from_radians(asin(x))

def arccos_degrees(x):
    """Return arccosine of x in degrees."""
    return normalized_degrees_from_radians(acos(x))

class DegreeMinutesSeconds(object):
    
    def __init__(self, degrees, minutes, seconds):
        self.degress = degrees
        self.minutes = minutes
        self.seconds = seconds

    @classmethod        
    def from_angle(cls, alpha):
        """Return an angle in degrees:minutes:seconds from angle,
        'alpha' in degrees."""
        d = ifloor(alpha)
        m = ifloor(60 * mod(alpha, 1))
        s = mod(alpha * 60 * 60, 60)
        return DegreeMinutesSeconds(d, m, s)
