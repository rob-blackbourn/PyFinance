from mpmath import atan2
from py_cal_cal import cos_degrees, sin_degrees, tan_degrees, arcsin_degrees
from py_cal_cal import normalized_degrees_from_radians

class ElipticalCoordinates(object):
    
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

    @classmethod        
    def from_equatorial(cls, ra, declination, obliquity):
        """Convert equatorial coordinates (in degrees) to ecliptical ones.
        'declination' is the declination,
        'ra' is the right ascension and
        'obliquity' is the obliquity of the ecliptic.
        NOTE: if 'apparent' right ascension and declination are used, then 'true'
              obliquity should be input.
        """
        co = cos_degrees(obliquity)
        so = sin_degrees(obliquity)
        sa = sin_degrees(ra)
        longitude = normalized_degrees_from_radians(atan2(sa*co + tan_degrees(declination)*so, cos_degrees(ra)))
        latitude = arcsin_degrees(sin_degrees(declination)*co - cos_degrees(declination)*so*sa)
        return ElipticalCoordinates(longitude, latitude)

class EquatorialCoordinates(object):
    
    def __init__(self, ra, declination):
        self.ra = ra
        self.declination = declination

    @classmethod        
    def from_ecliptical(cls, longitude, latitude, obliquity):
        """Convert ecliptical coordinates (in degrees) to equatorial ones.
        'longitude' is the ecliptical longitude,
        'latitude'  is the ecliptical latitude and
        'obliquity' is the obliquity of the ecliptic.
        NOTE: resuting 'ra' and 'declination' will be referred to the same equinox
              as the one of input ecliptical longitude and latitude.
        """
        co = cos_degrees(obliquity)
        so = sin_degrees(obliquity)
        sl = sin_degrees(longitude)
        ra = normalized_degrees_from_radians(atan2(sl*co - tan_degrees(latitude)*so, cos_degrees(longitude)))
        dec = arcsin_degrees(sin_degrees(latitude)*co + cos_degrees(latitude)*so*sl)
        return EquatorialCoordinates(ra, dec)

class HorizontalCoordinates(object):
    
    def __init__(self, azimuth, altitude):
        self.azimuth = azimuth
        self.altitude = altitude

    @classmethod        
    def horizontal_from_equatorial(cls, H, declination, latitude):
        """Convert equatorial coordinates (in degrees) to horizontal ones.
        Return 'azimuth' and 'altitude'.
        'H'            is the local hour angle,
        'declination'  is the declination,
        'latitude'     is the observer's geographic latitude.
        NOTE: 'azimuth' is measured westward from the South.
        NOTE: This is not a good formula for using near the poles.
        """
        ch = cos_degrees(H)
        sl = sin_degrees(latitude)
        cl = cos_degrees(latitude)
        azimuth = normalized_degrees_from_radians(atan2(sin_degrees(H), ch * sl - tan_degrees(declination) * cl))
        altitude = arcsin_degrees(sl * sin_degrees(declination) + cl * cos_degrees(declination) * ch)
        return HorizontalCoordinates(azimuth, altitude)

    def to_equatorial(self, phi):
        """Convert equatorial coordinates (in degrees) to horizontal ones.
        Return 'local hour angle' and 'declination'.
        'A'   is the azimuth,
        'h'   is the altitude,
        'phi' is the observer's geographical latitude.
        NOTE: 'azimuth' is measured westward from the South.
        """
        H = normalized_degrees_from_radians(
                atan2(sin_degrees(self.azimuth), 
                      (cos_degrees(self.azimuth) * sin_degrees(phi) + 
                       tan_degrees(self.altitude) * cos_degrees(phi))))
        delta = arcsin_degrees(sin_degrees(phi) * sin_degrees(self.altitude) - 
                               cos_degrees(phi) * cos_degrees(self.altitude) * cos_degrees(self.azimuth))
        return [H, delta]
