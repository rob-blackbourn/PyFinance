from operator import mod
from mpmath import mpf
import math
from py_calendrical.triganometry import sin_degrees, cos_degrees, tan_degrees, arctan_degrees, arcsin_degrees, arccos_degrees, secs, angle 
from py_calendrical.py_cal_cal import binary_search
from py_calendrical.astro import equation_of_time, solar_longitude, declination, lunar_phase
from py_calendrical.time_arithmatic import Clock

class Location(object):

    MORNING = True
    EVENING = False
    
    def __init__(self, latitude, longitude, elevation, zone):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.zone = zone

    def direction(self, focus):
        """Return the angle (clockwise from North) to face focus when
        standing in location, location.  Subject to errors near focus and
        its antipode."""
        phi = self.latitude
        phi_prime = focus.latitude
        psi = self.longitude
        psi_prime = focus.longitude
        y = sin_degrees(psi_prime - psi)
        x = ((cos_degrees(phi) * tan_degrees(phi_prime)) -
             (sin_degrees(phi)    * cos_degrees(psi - psi_prime)))
        if ((x == y == 0) or (phi_prime == 90)):
            return 0
        elif (phi_prime == -90):
            return 180
        else:
            return arctan_degrees(y, x)

    def standard_from_universal(self, tee_rom_u):
        """Return standard time from tee_rom_u in universal time at location."""
        return tee_rom_u + self.zone
    
    # see lines 2805-2809 in calendrica-3.0.cl
    def universal_from_standard(self, tee_rom_s):
        """Return universal time from tee_rom_s in standard time at location."""
        return tee_rom_s - self.zone

    @classmethod
    def zone_from_longitude(cls, phi):
        """Return the difference between UT and local mean time at longitude
        'phi' as a fraction of a day."""
        return phi / 360
    
    def local_from_universal(self, tee_rom_u):
        """Return local time from universal tee_rom_u at location, location."""
        return tee_rom_u + self.zone_from_longitude(self.longitude)
    
    def universal_from_local(self, tee_ell):
        """Return universal time from local tee_ell at location, location."""
        return tee_ell - self.zone_from_longitude(self.longitude)
    
    def standard_from_local(self, tee_ell):
        """Return standard time from local tee_ell at locale, location."""
        return self.standard_from_universal(self.universal_from_local(tee_ell))
    
    def local_from_standard(self, tee_rom_s):
        """Return local time from standard tee_rom_s at location, location."""
        return self.local_from_universal(self.universal_from_standard(tee_rom_s))
    
    # see lines 2841-2844 in calendrica-3.0.cl
    def apparent_from_local(self, tee):
        """Return sundial time at local time tee at location, location."""
        return tee + equation_of_time(self.universal_from_local(tee))
    
    # see lines 2846-2849 in calendrica-3.0.cl
    def local_from_apparent(self, tee):
        """Return local time from sundial time tee at location, location."""
        return tee - equation_of_time(self.universal_from_local(tee))
    
    # see lines 2851-2857 in calendrica-3.0.cl
    def midnight(self, date):
        """Return standard time on fixed date, date, of true (apparent)
        midnight at location, location."""
        return self.standard_from_local(self.local_from_apparent(date))
    
    # see lines 2859-2864 in calendrica-3.0.cl
    def midday(self, date):
        """Return standard time on fixed date, date, of midday
        at location, location."""
        return self.standard_from_local(self.local_from_apparent(date + Clock.days_from_hours(mpf(12))))

    def sine_offset(self, tee, alpha):
        """Return sine of angle between position of sun at 
        local time tee and when its depression is alpha at location, location.
        Out of range when it does not occur."""
        phi = self.latitude
        tee_prime = self.universal_from_local(tee)
        delta = declination(tee_prime, mpf(0), solar_longitude(tee_prime))
        return ((tan_degrees(phi) * tan_degrees(delta)) +
                (sin_degrees(alpha) / (cos_degrees(delta) *
                                       cos_degrees(phi))))

    # see lines 2922-2947 in calendrica-3.0.cl
    def approx_moment_of_depression(self, tee, alpha, early):
        """Return the moment in local time near tee when depression angle
        of sun is alpha (negative if above horizon) at location;
        early is true when MORNING event is sought and false for EVENING.
        Raise VlueError if depression angle is not reached."""
        ttry  = self.sine_offset(tee, alpha)
        date = Clock.fixed_from_moment(tee)
    
        if (alpha >= 0):
            if early:
                alt = date
            else:
                alt = date + 1
        else:
            alt = date + Clock.days_from_hours(12)
    
        if (abs(ttry) > 1):
            value = self.sine_offset(alt, alpha)
        else:
            value = ttry
    
    
        if (abs(value) <= 1):
            temp = -1 if early else 1
            temp *= mod(Clock.days_from_hours(12) + arcsin_degrees(value) / 360, 1) - Clock.days_from_hours(6)
            temp += date + Clock.days_from_hours(12)
            return self.local_from_apparent(temp)
        else:
            raise ValueError("Depression angle not reached")

    def moment_of_depression(self, approx, alpha, early):
        """Return the moment in local time near approx when depression
        angle of sun is alpha (negative if above horizon) at location;
        early is true when MORNING event is sought, and false for EVENING."""
        tee = self.approx_moment_of_depression(approx, alpha, early)
        if abs(approx - tee) < Clock.days_from_seconds(30):
            return tee
        else:
            return self.moment_of_depression(tee, alpha, early)

    def dawn(self, date, alpha):
        """Return standard time in morning on fixed date date at
        location location when depression angle of sun is alpha."""
        result = self.moment_of_depression(date + Clock.days_from_hours(6), alpha, self.MORNING)
        return self.standard_from_local(result)
    
    def dusk(self, date, alpha):
        """Return standard time in evening on fixed date 'date' at
        location 'location' when depression angle of sun is alpha."""
        result = self.moment_of_depression(date + Clock.days_from_hours(18), alpha, self.EVENING)
        return self.standard_from_local(result)

    def refraction(self, tee):
        """Return refraction angle at location 'location' and time 'tee'."""
        h     = max(0, self.elevation)
        cap_R = 6.372E6
        dip   = arccos_degrees(cap_R / (cap_R + h))
        return angle(0, 50, 0) + dip + secs(19) * math.sqrt(h)

    def sunrise(self, date):
        """Return Standard time of sunrise on fixed date 'date' at
        location 'location'."""
        alpha = self.refraction(date)
        return self.dawn(date, alpha)
    
    def sunset(self, date):
        """Return standard time of sunset on fixed date 'date' at
        location 'location'."""
        alpha = self.refraction(date)
        return self.dusk(date, alpha)
    
    def observed_lunar_altitude(self, tee):
        """Return the observed altitude of moon at moment, tee, and
        at location, location,  taking refraction into account."""
        return self.topocentric_lunar_altitude(tee) + self.refraction(tee)
    
    def moonrise(self, date):
        """Return the standard time of moonrise on fixed, date,
        and location, location."""
        t = self.universal_from_standard(date)
        waning = (lunar_phase(t) > 180)
        alt = self.observed_lunar_altitude(t)
        offset = alt / 360
        if (waning and (offset > 0)):
            approx =  t + 1 - offset
        elif waning:
            approx = t - offset
        else:
            approx = t + (1 / 2) + offset
        rise = binary_search(approx - Clock.days_from_hours(3),
                             approx + Clock.days_from_hours(3),
                             lambda u, l: ((u - l) < Clock.days_from_hours(1 / 60)),
                             lambda x: self.observed_lunar_altitude(x) > 0)
        if (rise < (t + 1)):
            return self.standard_from_universal(rise)
        
        raise ValueError()

    def daytime_temporal_hour(self, date):
        """Return the length of daytime temporal hour on fixed date, date
        at location, location."""
        return (self.sunset(date) - self.sunrise(date)) / 12
    
    def nighttime_temporal_hour(self, date):
        """Return the length of nighttime temporal hour on fixed date, date,
        at location, location."""
        return (self.sunrise(date + 1) - self.sunset(date)) / 12

MECCA = Location(angle(21, 25, 24), angle(39, 49, 24), 298, Clock.days_from_hours(3))
JERUSALEM = Location(31.8, 35.2, 800, Clock.days_from_hours(2))
BRUXELLES = Location(angle(4, 21, 17), angle(50, 50, 47), 800, Clock.days_from_hours(1))
URBANA = Location(40.1, -88.2, 225, Clock.days_from_hours(-6))
GREENWHICH = Location(51.4777815, 0, 46.9, Clock.days_from_hours(0))
