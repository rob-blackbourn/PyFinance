from __future__ import division
from operator import mod
from mpmath import mpf
import math
from py_calendrical.triganometry import sin_degrees, cos_degrees, tan_degrees, arctan_degrees, arcsin_degrees, arccos_degrees, secs, angle 
from py_calendrical.py_cal_cal import binary_search, ifloor
from py_calendrical.time_arithmatic import Clock
from py_calendrical.utils import next_int
from py_calendrical.lunar import Lunar
from py_calendrical.astro import Astro
from py_calendrical.solar import Solar

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
        y = sin_degrees(focus.longitude - self.longitude)
        x = ((cos_degrees(self.latitude) * tan_degrees(focus.latitude)) -
             (sin_degrees(self.latitude) * cos_degrees(self.longitude - focus.longitude)))
        if x == y == 0 or focus.latitude == 90:
            return 0
        elif focus.latitude == -90:
            return 180
        else:
            return arctan_degrees(y, x)

    def standard_from_universal(self, universal_time):
        """Return standard time from universal time at this location."""
        return universal_time + self.zone
    
    def universal_from_standard(self, standard_time):
        """Return universal time from standard time at this location."""
        return standard_time - self.zone
    
    def local_from_universal(self, universal_time):
        """Return local time from universal time at this location."""
        return universal_time + Astro.zone_from_longitude(self.longitude)
    
    def universal_from_local(self, local_time):
        """Return universal time from local time at this location."""
        return local_time - Astro.zone_from_longitude(self.longitude)
    
    def standard_from_local(self, local_time):
        """Return standard time from local time at this location."""
        return self.standard_from_universal(self.universal_from_local(local_time))
    
    def local_from_standard(self, standard_time):
        """Return local time from standard time at this location."""
        return self.local_from_universal(self.universal_from_standard(standard_time))

    def apparent_from_local(self, local_time):
        """Return sundial time from local time at this location."""
        return local_time + Astro.equation_of_time(self.universal_from_local(local_time))
    
    def local_from_apparent(self, tee):
        """Return local time from sundial time tee at location, location."""
        return tee - Astro.equation_of_time(self.universal_from_local(tee))
    
    def midnight(self, date):
        """Return standard time on fixed date, date, of true (apparent)
        midnight at location, location."""
        return self.standard_from_local(self.local_from_apparent(date))
    
    def midday(self, date):
        """Return standard time on fixed date, date, of midday
        at location, location."""
        return self.standard_from_local(self.local_from_apparent(date + Clock.days_from_hours(mpf(12))))

    def sine_offset(self, local_time, alpha):
        """Return sine of angle between position of sun at 
        local time tee and when its depression is alpha at location, location.
        Out of range when it does not occur."""
        phi = self.latitude
        tee_prime = self.universal_from_local(local_time)
        delta = Astro.declination(tee_prime, mpf(0), Solar.solar_longitude(tee_prime))
        return ((tan_degrees(phi) * tan_degrees(delta)) +
                (sin_degrees(alpha) / (cos_degrees(delta) *
                                       cos_degrees(phi))))

    def approx_moment_of_depression(self, tee, alpha, early):
        """Return the moment in local time near tee when depression angle
        of sun is alpha (negative if above horizon) at location;
        early is true when MORNING event is sought and false for EVENING.
        Raise VlueError if depression angle is not reached."""
        ttry  = self.sine_offset(tee, alpha)
        date = Clock.fixed_from_moment(tee)
    
        if alpha >= 0:
            if early:
                alt = date
            else:
                alt = date + 1
        else:
            alt = date + Clock.days_from_hours(12)
    
        if abs(ttry) > 1:
            value = self.sine_offset(alt, alpha)
        else:
            value = ttry
    
        if abs(value) <= 1:
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
        waning = (Lunar.lunar_phase(t) > 180)
        alt = self.observed_lunar_altitude(t)
        offset = alt / 360
        if waning and (offset > 0):
            approx =  t + 1 - offset
        elif waning:
            approx = t - offset
        else:
            approx = t + (1 / 2) + offset
        rise = binary_search(approx - Clock.days_from_hours(3),
                             approx + Clock.days_from_hours(3),
                             lambda u, l: ((u - l) < Clock.days_from_hours(1/60)),
                             lambda x: self.observed_lunar_altitude(x) > 0)
        if rise < (t + 1):
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

    def standard_from_sundial(self, tee):
        """Return standard time of temporal moment, tee, at location, location."""
        date = Clock.fixed_from_moment(tee)
        hour = 24 * mod(tee, 1)
        if 6 <= hour <= 18:
            h = self.daytime_temporal_hour(date)
        elif (hour < 6):
            h = self.nighttime_temporal_hour(date - 1)
        else:
            h = self.nighttime_temporal_hour(date)
    
        # return
        if 6 <= hour <= 18:
            return self.sunrise(date) + ((hour - 6) * h)
        elif hour < 6:
            return self.sunset(date - 1) + ((hour + 6) * h)
        else:
            return self.sunset(date) + ((hour - 18) * h)
    
    def lunar_parallax(self, tee):
        """Return the parallax of moon at moment, tee, at location, location.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1998."""
        geo = self.lunar_altitude(tee)
        Delta = Lunar.lunar_distance(tee)
        alt = 6378140 / Delta
        arg = alt * cos_degrees(geo)
        return arcsin_degrees(arg)
    
    def topocentric_lunar_altitude(self, tee):
        """Return the topocentric altitude of moon at moment, tee,
        at location, location, as a small positive/negative angle in degrees,
        ignoring refraction."""
        return self.lunar_altitude(tee) - self.lunar_parallax(tee)
    
    def phasis_on_or_before(self, date):
        """Return the closest fixed date on or before date 'date', when crescent
        moon first became visible at location 'location'."""
        mean = date - ifloor(Lunar.lunar_phase(date + 1) / 360.0 * Lunar.MEAN_SYNODIC_MONTH)
        tau = ((mean - 30)
               if (((date - mean) <= 3) and (not self.visible_crescent(date)))
               else (mean - 2))
        return  next_int(tau, lambda d: self.visible_crescent(d))

    def lunar_altitude(self, tee):
        """Return the geocentric altitude of moon at moment, tee,
        at location, location, as a small positive/negative angle in degrees,
        ignoring parallax and refraction.  Adapted from 'Astronomical
        Algorithms' by Jean Meeus, Willmann_Bell, Inc., 1998."""
        lamb = Lunar.lunar_longitude(tee)
        beta = Lunar.lunar_latitude(tee)
        alpha = Astro.right_ascension(tee, beta, lamb)
        delta = Astro.declination(tee, beta, lamb)
        theta0 = Astro.sidereal_from_moment(tee)
        cap_H = mod(theta0 + self.longitude - alpha, 360)
        altitude = arcsin_degrees(
            (sin_degrees(self.latitude) * sin_degrees(delta)) +
            (cos_degrees(self.latitude) * cos_degrees(delta) * cos_degrees(cap_H)))
        return mod(altitude + 180, 360) - 180

    @classmethod
    def visible_crescent(self, date):
        """Return S. K. Shaukat's criterion for likely
        visibility of crescent moon on eve of date 'date',
        at location 'location'."""
        tee = self.universal_from_standard(self.dusk(date - 1, mpf(4.5)))
        phase = self.lunar_phase(tee)
        altitude = self.lunar_altitude(tee)
        arc_of_light = arccos_degrees(cos_degrees(self.lunar_latitude(tee)) * cos_degrees(phase))
        return ((Lunar.NEW < phase < Lunar.FIRST_QUARTER) and
                (mpf(10.6) <= arc_of_light <= 90) and
                (altitude > mpf(4.1)))

MECCA = Location(angle(21, 25, 24), angle(39, 49, 24), 298, Clock.days_from_hours(3))
JERUSALEM = Location(31.8, 35.2, 800, Clock.days_from_hours(2))
BRUXELLES = Location(angle(4, 21, 17), angle(50, 50, 47), 800, Clock.days_from_hours(1))
URBANA = Location(40.1, -88.2, 225, Clock.days_from_hours(-6))
GREENWHICH = Location(51.4777815, 0, 46.9, Clock.days_from_hours(0))
