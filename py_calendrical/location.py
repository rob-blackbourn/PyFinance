from operator import mod
from mpmath import mpf, pi
import math
from py_calendrical.triganometry import sin_degrees, cos_degrees, tan_degrees, arctan_degrees, arcsin_degrees, arccos_degrees, secs, angle, normalized_degrees 
from py_calendrical.py_cal_cal import binary_search, ifloor, iround, poly, signum, sigma, final_int, next_int, invert_angular
from py_calendrical.time_arithmatic import Clock
from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth

class Location(object):

    MORNING = True
    EVENING = False

    J2000 = Clock.days_from_hours(mpf(12)) + GregorianDate.new_year(2000)
    
    MEAN_TROPICAL_YEAR = mpf(365.242189)
    MEAN_SIDEREAL_YEAR = mpf(365.25636)
    MEAN_SYNODIC_MONTH = mpf(29.530588861)
    
    SPRING = 0
    SUMMER = 90
    AUTUMN = 180
    WINTER = 270
    
    NEW = 0
    FIRST_QUARTER = 90
    FULL = 180
    LAST_QUARTER = 270

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

    def standard_from_universal(self, tee_rom_u):
        """Return standard time from tee_rom_u in universal time at location."""
        return tee_rom_u + self.zone
    
    def universal_from_standard(self, tee_rom_s):
        """Return universal time from tee_rom_s in standard time at location."""
        return tee_rom_s - self.zone

    @classmethod
    def zone_from_longitude(cls, phi):
        """Return the difference between UT and local mean time at longitude
        'phi' as a fraction of a day."""
        return phi / 360.0
    
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
    
    @classmethod    
    def ephemeris_correction(cls, tee):
        """Return Dynamical Time minus Universal Time (in days) for
        moment, tee.  Adapted from "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 1991."""
        year = GregorianDate.to_year(ifloor(tee))
        c = GregorianDate.date_difference(GregorianDate(1900, JulianMonth.January, 1), GregorianDate(year, JulianMonth.July, 1)) / mpf(36525)
        if (1988 <= year <= 2019):
            return 1.0 / 86400.0 * (year - 1933)
        elif (1900 <= year <= 1987):
            return poly(c, [mpf(-0.00002), mpf(0.000297), mpf(0.025184), mpf(-0.181133), mpf(0.553040), mpf(-0.861938), mpf(0.677066), mpf(-0.212591)])
        elif (1800 <= year <= 1899):
            return poly(c, [mpf(-0.000009), mpf(0.003844), mpf(0.083563), mpf(0.865736), mpf(4.867575), mpf(15.845535), mpf(31.332267), mpf(38.291999), mpf(28.316289), mpf(11.636204), mpf(2.043794)])
        elif (1700 <= year <= 1799):
            return (1.0 / 86400.0 * poly(year - 1700, [8.118780842, -0.005092142, 0.003336121, -0.0000266484]))
        elif (1620 <= year <= 1699):
            return (1.0 / 86400.0 * poly(year - 1600, [mpf(196.58333), mpf(-4.0675), mpf(0.0219167)]))
        else:
            x = (Clock.days_from_hours(mpf(12)) + GregorianDate.date_difference(GregorianDate(1810, JulianMonth.January, 1), GregorianDate(year, JulianMonth.January, 1)))
            return 1.0 / 86400.0 * (((x * x) / mpf(41048480)) - 15)

    @classmethod
    def universal_from_dynamical(cls, tee):
        """Return Universal moment from Dynamical time, tee."""
        return tee - cls.ephemeris_correction(tee)

    @classmethod
    def dynamical_from_universal(cls, tee):
        """Return Dynamical time at Universal moment, tee."""
        return tee + cls.ephemeris_correction(tee)

    @classmethod
    def julian_centuries(cls, tee):
        """Return Julian centuries since 2000 at moment tee."""
        return (cls.dynamical_from_universal(tee) - cls.J2000) / mpf(36525)

    @classmethod
    def obliquity(cls, tee):
        """Return (mean) obliquity of ecliptic at moment tee."""
        c = cls.julian_centuries(tee)
        return (angle(23, 26, mpf(21.448)) +
                poly(c, [mpf(0),
                         angle(0, 0, mpf(-46.8150)),
                         angle(0, 0, mpf(-0.00059)),
                         angle(0, 0, mpf(0.001813))]))

    @classmethod
    def equation_of_time(cls, tee):
        """Return the equation of time (as fraction of day) for moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1991."""
        c = cls.julian_centuries(tee)
        lamb = poly(c, [mpf(280.46645), mpf(36000.76983), mpf(0.0003032)])
        anomaly = poly(c, [mpf(357.52910), mpf(35999.05030), mpf(-0.0001559), mpf(-0.00000048)])
        eccentricity = poly(c, [mpf(0.016708617), mpf(-0.000042037), mpf(-0.0000001236)])
        varepsilon = cls.obliquity(tee)
        y = pow(tan_degrees(varepsilon / 2.0), 2)
        equation = ((1.0 / 2.0 / pi) *
                    (y * sin_degrees(2 * lamb) +
                     -2 * eccentricity * sin_degrees(anomaly) +
                     (4 * eccentricity * y * sin_degrees(anomaly) *
                      cos_degrees(2 * lamb)) +
                     -0.5 * y * y * sin_degrees(4 * lamb) +
                     -1.25 * eccentricity * eccentricity * sin_degrees(2 * anomaly)))
        return signum(equation) * min(abs(equation), Clock.days_from_hours(mpf(12)))

    def apparent_from_local(self, tee):
        """Return sundial time at local time tee at location, location."""
        return tee + self.equation_of_time(self.universal_from_local(tee))
    
    def local_from_apparent(self, tee):
        """Return local time from sundial time tee at location, location."""
        return tee - self.equation_of_time(self.universal_from_local(tee))
    
    def midnight(self, date):
        """Return standard time on fixed date, date, of true (apparent)
        midnight at location, location."""
        return self.standard_from_local(self.local_from_apparent(date))
    
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
        delta = self.declination(tee_prime, mpf(0), self.solar_longitude(tee_prime))
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
            temp *= mod(Clock.days_from_hours(12) + arcsin_degrees(value) / 360.0, 1) - Clock.days_from_hours(6)
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
        waning = (self.lunar_phase(t) > 180)
        alt = self.observed_lunar_altitude(t)
        offset = alt / 360.0
        if waning and (offset > 0):
            approx =  t + 1 - offset
        elif waning:
            approx = t - offset
        else:
            approx = t + (1 / 2) + offset
        rise = binary_search(approx - Clock.days_from_hours(3),
                             approx + Clock.days_from_hours(3),
                             lambda u, l: ((u - l) < Clock.days_from_hours(1.0 / 60.0)),
                             lambda x: self.observed_lunar_altitude(x) > 0)
        if rise < (t + 1):
            return self.standard_from_universal(rise)
        
        raise ValueError()

    def daytime_temporal_hour(self, date):
        """Return the length of daytime temporal hour on fixed date, date
        at location, location."""
        return (self.sunset(date) - self.sunrise(date)) / 12.0
    
    def nighttime_temporal_hour(self, date):
        """Return the length of nighttime temporal hour on fixed date, date,
        at location, location."""
        return (self.sunrise(date + 1) - self.sunset(date)) / 12.0

    @classmethod
    def precise_obliquity(cls, tee):
        """Return precise (mean) obliquity of ecliptic at moment tee."""
        u = cls.julian_centuries(tee) / 100.0
        #assert(abs(u) < 1,
        #       'Error! This formula is valid for +/-10000 years around J2000.0')
        return (poly(u, [angle(23, 26, mpf(21.448)),
                         angle(0, 0, mpf(-4680.93)),
                         angle(0, 0, mpf(-   1.55)),
                         angle(0, 0, mpf(+1999.25)),
                         angle(0, 0, mpf(-  51.38)),
                         angle(0, 0, mpf(- 249.67)),
                         angle(0, 0, mpf(-  39.05)),
                         angle(0, 0, mpf(+   7.12)),
                         angle(0, 0, mpf(+  27.87)),
                         angle(0, 0, mpf(+   5.79)),
                         angle(0, 0, mpf(+   2.45))]))

    @classmethod
    def declination(cls, tee, beta, lam):
        """Return declination at moment UT tee of object at
        longitude 'lam' and latitude 'beta'."""
        varepsilon = cls.obliquity(tee)
        return arcsin_degrees(
            (sin_degrees(beta) * cos_degrees(varepsilon)) +
            (cos_degrees(beta) * sin_degrees(varepsilon) * sin_degrees(lam)))
    
    @classmethod
    def right_ascension(cls, tee, beta, lam):
        """Return right ascension at moment UT 'tee' of object at
        latitude 'lam' and longitude 'beta'."""
        varepsilon = cls.obliquity(tee)
        return arctan_degrees((sin_degrees(lam) * cos_degrees(varepsilon)) - (tan_degrees(beta) * sin_degrees(varepsilon)), cos_degrees(lam))

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

    @classmethod
    def sidereal_from_moment(cls, tee):
        """Return the mean sidereal time of day from moment tee expressed
        as hour angle.  Adapted from "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 1991."""
        c = (tee - cls.J2000) / mpf(36525)
        return mod(poly(c, [mpf(280.46061837), mpf(36525) * mpf(360.98564736629), mpf(0.000387933), mpf(-1)/mpf(38710000)]), 360)

    @classmethod
    def solar_latitude(cls, tee):
        """Return the latitude of Sun (in degrees) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1998."""
        pass
    
    @classmethod
    def solar_distance(cls, tee):
        """Return the distance of Sun (in degrees) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1998."""
        pass

    @classmethod
    def solar_longitude(cls, tee):
        """Return the longitude of sun at moment 'tee'.
        Adapted from 'Planetary Programs and Tables from -4000 to +2800'
        by Pierre Bretagnon and Jean_Louis Simon, Willmann_Bell, Inc., 1986.
        See also pag 166 of 'Astronomical Algorithms' by Jean Meeus, 2nd Ed 1998,
        with corrections Jun 2005."""
        c = cls.julian_centuries(tee)
        coefficients = [403406, 195207, 119433, 112392, 3891, 2819, 1721,
                        660, 350, 334, 314, 268, 242, 234, 158, 132, 129, 114,
                        99, 93, 86, 78,72, 68, 64, 46, 38, 37, 32, 29, 28, 27, 27,
                        25, 24, 21, 21, 20, 18, 17, 14, 13, 13, 13, 12, 10, 10, 10,
                        10]
        multipliers = [mpf(0.9287892), mpf(35999.1376958), mpf(35999.4089666),
                       mpf(35998.7287385), mpf(71998.20261), mpf(71998.4403),
                       mpf(36000.35726), mpf(71997.4812), mpf(32964.4678),
                       mpf(-19.4410), mpf(445267.1117), mpf(45036.8840), mpf(3.1008),
                       mpf(22518.4434), mpf(-19.9739), mpf(65928.9345),
                       mpf(9038.0293), mpf(3034.7684), mpf(33718.148), mpf(3034.448),
                       mpf(-2280.773), mpf(29929.992), mpf(31556.493), mpf(149.588),
                       mpf(9037.750), mpf(107997.405), mpf(-4444.176), mpf(151.771),
                       mpf(67555.316), mpf(31556.080), mpf(-4561.540),
                       mpf(107996.706), mpf(1221.655), mpf(62894.167),
                       mpf(31437.369), mpf(14578.298), mpf(-31931.757),
                       mpf(34777.243), mpf(1221.999), mpf(62894.511),
                       mpf(-4442.039), mpf(107997.909), mpf(119.066), mpf(16859.071),
                       mpf(-4.578), mpf(26895.292), mpf(-39.127), mpf(12297.536),
                       mpf(90073.778)]
        addends = [mpf(270.54861), mpf(340.19128), mpf(63.91854), mpf(331.26220),
                   mpf(317.843), mpf(86.631), mpf(240.052), mpf(310.26), mpf(247.23),
                   mpf(260.87), mpf(297.82), mpf(343.14), mpf(166.79), mpf(81.53),
                   mpf(3.50), mpf(132.75), mpf(182.95), mpf(162.03), mpf(29.8),
                   mpf(266.4), mpf(249.2), mpf(157.6), mpf(257.8),mpf(185.1),
                   mpf(69.9),  mpf(8.0), mpf(197.1), mpf(250.4), mpf(65.3),
                   mpf(162.7), mpf(341.5), mpf(291.6), mpf(98.5), mpf(146.7),
                   mpf(110.0), mpf(5.2), mpf(342.6), mpf(230.9), mpf(256.1),
                   mpf(45.3), mpf(242.9), mpf(115.2), mpf(151.8), mpf(285.3),
                   mpf(53.3), mpf(126.6), mpf(205.7), mpf(85.9), mpf(146.1)]
        lam = (mpf(282.7771834) +
               mpf(36000.76953744) * c +
               mpf(0.000005729577951308232) *
               sigma([coefficients, addends, multipliers],
                     lambda x, y, z:  x * sin_degrees(y + (z * c))))
        return mod(lam + cls.aberration(tee) + cls.nutation(tee), 360)

    @classmethod
    def geometric_solar_mean_longitude(cls, tee):
        """Return the geometric mean longitude of the Sun at moment, tee,
        referred to mean equinox of the date."""
        c = cls.julian_centuries(tee)
        return poly(c, [mpf(280.46646), mpf(36000.76983), mpf(0.0003032)])

    @classmethod
    def nutation(cls, tee):
        """Return the longitudinal nutation at moment, tee."""
        c = cls.julian_centuries(tee)
        cap_A = poly(c, [mpf(124.90), mpf(-1934.134), mpf(0.002063)])
        cap_B = poly(c, [mpf(201.11), mpf(72001.5377), mpf(0.00057)])
        return (mpf(-0.004778)  * sin_degrees(cap_A) + 
                mpf(-0.0003667) * sin_degrees(cap_B))
    
    @classmethod
    def aberration(cls, tee):
        """Return the aberration at moment, tee."""
        c = cls.julian_centuries(tee)
        return ((mpf(0.0000974) *
                 cos_degrees(mpf(177.63) + mpf(35999.01848) * c)) -
                mpf(0.005575))

    @classmethod
    def solar_position(cls, tee):
        """Return the position of the Sun (geocentric latitude and longitude [in degrees]
        and distance [in meters]) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed."""
        return (cls.solar_latitude(tee), cls.solar_longitude(tee), cls.solar_distance(tee))
    
    @classmethod
    def solar_longitude_after(cls, lam, tee):
        """Return the moment UT of the first time at or after moment, tee,
        when the solar longitude will be lam degrees."""
        rate = cls.MEAN_TROPICAL_YEAR / 360.0
        tau = tee + rate * mod(lam - cls.solar_longitude(tee), 360)
        a = max(tee, tau - 5)
        b = tau + 5
        return invert_angular(cls.solar_longitude, lam, a, b)

    @classmethod
    def precession(cls, tee):
        """Return the precession at moment tee using 0,0 as J2000 coordinates.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann-Bell, Inc., 1991."""
        c = cls.julian_centuries(tee)
        eta = mod(poly(c, [0, secs(mpf(47.0029)), secs(mpf(-0.03302)), secs(mpf(0.000060))]), 360)
        cap_P = mod(poly(c, [mpf(174.876384), secs(mpf(-869.8089)), secs(mpf(0.03536))]), 360)
        p = mod(poly(c, [0, secs(mpf(5029.0966)), secs(mpf(1.11113)), secs(mpf(0.000006))]), 360)
        cap_A = cos_degrees(eta) * sin_degrees(cap_P)
        cap_B = cos_degrees(cap_P)
        arg = arctan_degrees(cap_A, cap_B)
    
        return mod(p + cap_P - arg, 360)
    
    @classmethod
    def estimate_prior_solar_longitude(cls, lam, tee):
        """Return approximate moment at or before tee
        when solar longitude just exceeded lam degrees."""
        rate = cls.MEAN_TROPICAL_YEAR / 360.0
        tau = tee - (rate * mod(cls.solar_longitude(tee) - lam, 360))
        cap_Delta = mod(cls.solar_longitude(tau) - lam + 180, 360) - 180
        return min(tee, tau - (rate * cap_Delta))
    
    @classmethod
    def mean_lunar_longitude(cls, c):
        """Return mean longitude of moon (in degrees) at moment
        given in Julian centuries c (including the constant term of the
        effect of the light-time (-0".70).
        Adapted from eq. 47.1 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(218.3164477), mpf(481267.88123421),
                                   mpf(-0.0015786), mpf(1.0 / 538841.0),
                                   mpf(-1.0 / 65194000.0)]))
    
    @classmethod
    def lunar_elongation(cls, c):
        """Return elongation of moon (in degrees) at moment
        given in Julian centuries c.
        Adapted from eq. 47.2 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(297.8501921), mpf(445267.1114034),
                                    mpf(-0.0018819), mpf(1.0 / 545868.0),
                                    mpf(-1.0 / 113065000.0)]))
    
    @classmethod
    def solar_anomaly(cls, c):
        """Return mean anomaly of sun (in degrees) at moment
        given in Julian centuries c.
        Adapted from eq. 47.3 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(357.5291092), mpf(35999.0502909), mpf(-0.0001536), mpf(1.0/24490000.0)]))
    
    @classmethod
    def lunar_anomaly(cls, c):
        """Return mean anomaly of moon (in degrees) at moment
        given in Julian centuries c.
        Adapted from eq. 47.4 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(134.9633964), mpf(477198.8675055), mpf(0.0087414), mpf(1.0/69699.0), mpf(-1.0/14712000.0)]))
    
    @classmethod
    def moon_node(cls, c):
        """Return Moon's argument of latitude (in degrees) at moment
        given in Julian centuries 'c'.
        Adapted from eq. 47.5 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(93.2720950), mpf(483202.0175233), mpf(-0.0036539), mpf(-1.0/3526000.0), mpf(1.0/863310000.0)]))
    
    @classmethod
    def lunar_longitude(cls, tee):
        """Return longitude of moon (in degrees) at moment tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed., 1998."""
        c = cls.julian_centuries(tee)
        cap_L_prime = cls.mean_lunar_longitude(c)
        cap_D = cls.lunar_elongation(c)
        cap_M = cls.solar_anomaly(c)
        cap_M_prime = cls.lunar_anomaly(c)
        cap_F = cls.moon_node(c)
        # see eq. 47.6 in Meeus
        cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
        args_lunar_elongation = \
                [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1,
                 1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2,
                 2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2]
        args_solar_anomaly = \
                [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
                 0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1,
                 -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0]
        args_lunar_anomaly = \
                [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2,
                 -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0,
                 -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3,
                 2, 1, -1, 3]
        args_moon_node = \
                [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0,
                 0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0]
        sine_coefficients = \
                [6288774,1274027,658314,213618,-185116,-114332,
                 58793,57066,53322,45758,-40923,-34720,-30383,
                 15327,-12528,10980,10675,10034,8548,-7888,
                 -6766,-5163,4987,4036,3994,3861,3665,-2689,
                 -2602, 2390,-2348,2236,-2120,-2069,2048,-1773,
                 -1595,1215,-1110,-892,-810,759,-713,-700,691,
                 596,549,537,520,-487,-399,-381,351,-340,330,
                 327,-323,299,294]
        correction = ((1.0/1000000.0) *
                      sigma([sine_coefficients, args_lunar_elongation,
                             args_solar_anomaly, args_lunar_anomaly,
                             args_moon_node],
                            lambda v, w, x, y, z:
                            v * pow(cap_E, abs(x)) *
                            sin_degrees((w * cap_D) +
                                        (x * cap_M) +
                                        (y * cap_M_prime) +
                                        (z * cap_F))))
        A1 = mpf(119.75) + (c * mpf(131.849))
        venus = ((3958.0/1000000.0) * sin_degrees(A1))
        A2 = mpf(53.09) + c * mpf(479264.29)
        jupiter = ((318.0/1000000.0) * sin_degrees(A2))
        flat_earth = ((1962.0/1000000.0) * sin_degrees(cap_L_prime - cap_F))
    
        return mod(cap_L_prime + correction + venus +
                   jupiter + flat_earth + cls.nutation(tee), 360)
    
    @classmethod
    def lunar_latitude(cls, tee):
        """Return the latitude of moon (in degrees) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1998."""
        c = cls.julian_centuries(tee)
        cap_L_prime = cls.mean_lunar_longitude(c)
        cap_D = cls.lunar_elongation(c)
        cap_M = cls.solar_anomaly(c)
        cap_M_prime = cls.lunar_anomaly(c)
        cap_F = cls.moon_node(c)
        cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
        args_lunar_elongation = \
                [0, 0, 0, 2, 2, 2, 2, 0, 2, 0, 2, 2, 2, 2, 2, 2, 2, 0, 4, 0, 0, 0,
                 1, 0, 0, 0, 1, 0, 4, 4, 0, 4, 2, 2, 2, 2, 0, 2, 2, 2, 2, 4, 2, 2,
                 0, 2, 1, 1, 0, 2, 1, 2, 0, 4, 4, 1, 4, 1, 4, 2]
        args_solar_anomaly = \
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 1, -1, -1, -1, 1, 0, 1,
                 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 1,
                 0, -1, -2, 0, 1, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0, 0, -1, -2]
        args_lunar_anomaly = \
                [0, 1, 1, 0, -1, -1, 0, 2, 1, 2, 0, -2, 1, 0, -1, 0, -1, -1, -1,
                 0, 0, -1, 0, 1, 1, 0, 0, 3, 0, -1, 1, -2, 0, 2, 1, -2, 3, 2, -3,
                 -1, 0, 0, 1, 0, 1, 1, 0, 0, -2, -1, 1, -2, 2, -2, -1, 1, 1, -2,
                 0, 0]
        args_moon_node = \
                [1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1,
                 -1, 1, 3, 1, 1, 1, -1, -1, -1, 1, -1, 1, -3, 1, -3, -1, -1, 1,
                 -1, 1, -1, 1, 1, 1, 1, -1, 3, -1, -1, 1, -1, -1, 1, -1, 1, -1,
                 -1, -1, -1, -1, -1, 1]
        sine_coefficients = \
                [5128122, 280602, 277693, 173237, 55413, 46271, 32573,
                 17198, 9266, 8822, 8216, 4324, 4200, -3359, 2463, 2211,
                 2065, -1870, 1828, -1794, -1749, -1565, -1491, -1475,
                 -1410, -1344, -1335, 1107, 1021, 833, 777, 671, 607,
                 596, 491, -451, 439, 422, 421, -366, -351, 331, 315,
                 302, -283, -229, 223, 223, -220, -220, -185, 181,
                 -177, 176, 166, -164, 132, -119, 115, 107]
        beta = ((1.0/1000000.0) *
                sigma([sine_coefficients, 
                       args_lunar_elongation,
                       args_solar_anomaly,
                       args_lunar_anomaly,
                       args_moon_node],
                      lambda v, w, x, y, z: (v *
                                             pow(cap_E, abs(x)) *
                                             sin_degrees((w * cap_D) +
                                                         (x * cap_M) +
                                                         (y * cap_M_prime) +
                                                         (z * cap_F)))))
        venus = ((175.0/1000000.0) *
                 (sin_degrees(mpf(119.75) + c * mpf(131.849) + cap_F) +
                  sin_degrees(mpf(119.75) + c * mpf(131.849) - cap_F)))
        flat_earth = ((-2235.0/1000000.0) *  sin_degrees(cap_L_prime) +
                      (127.0/1000000.0) * sin_degrees(cap_L_prime - cap_M_prime) +
                      (-115.0/1000000.0) * sin_degrees(cap_L_prime + cap_M_prime))
        extra = ((382.0/1000000.0) *
                 sin_degrees(mpf(313.45) + c * mpf(481266.484)))
        return beta + venus + flat_earth + extra
    
    @classmethod
    def lunar_node(cls, tee):
        """Return Angular distance of the node from the equinoctal point
        at fixed moment, tee.
        Adapted from eq. 47.7 in "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
        with corrections June 2005."""
        return mod(cls.moon_node(cls.julian_centuries(tee)) + 90, 180) - 90
    
    @classmethod
    def alt_lunar_node(cls, tee):
        """Return Angular distance of the node from the equinoctal point
        at fixed moment, tee.
        Adapted from eq. 47.7 in "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
        with corrections June 2005."""
        return normalized_degrees(poly(cls.julian_centuries(tee), [mpf(125.0445479), mpf(-1934.1362891), mpf(0.0020754), mpf(1.0/467441.0), mpf(-1.0/60616000.0)]))
    
    @classmethod
    def lunar_true_node(cls, tee):
        """Return Angular distance of the true node (the node of the instantaneus
        lunar orbit) from the equinoctal point at moment, tee.
        Adapted from eq. 47.7 and pag. 344 in "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
        with corrections June 2005."""
        c = cls.julian_centuries(tee)
        cap_D = cls.lunar_elongation(c)
        cap_M = cls.solar_anomaly(c)
        cap_M_prime = cls.lunar_anomaly(c)
        cap_F = cls.moon_node(c)
        periodic_terms = (-1.4979 * sin_degrees(2 * (cap_D - cap_F)) +
                          -0.1500 * sin_degrees(cap_M) +
                          -0.1226 * sin_degrees(2 * cap_D) +
                          0.1176  * sin_degrees(2 * cap_F) +
                          -0.0801 * sin_degrees(2 * (cap_M_prime - cap_F)))
        return cls.alt_lunar_node(tee) + periodic_terms
    
    @classmethod
    def lunar_perigee(cls, tee):
        """Return Angular distance of the perigee from the equinoctal point
        at moment, tee.
        Adapted from eq. 47.7 in "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998
        with corrections June 2005."""
        return normalized_degrees(poly(cls.julian_centuries(tee), [mpf(83.3532465), mpf(4069.0137287), mpf(-0.0103200), mpf(-1.0/80053.0), mpf(1.0/18999000.0)]))
    
    @classmethod
    def nth_new_moon(cls, n):
        """Return the moment of n-th new moon after (or before) the new moon
        of January 11, 1.  Adapted from "Astronomical Algorithms"
        by Jean Meeus, Willmann_Bell, Inc., 2nd ed., 1998."""
        n0 = 24724
        k = n - n0
        c = k / mpf(1236.85)
        approx = (cls.J2000 +
                  poly(c, [mpf(5.09766),
                           cls.MEAN_SYNODIC_MONTH * mpf(1236.85),
                           mpf(0.0001437),
                           mpf(-0.000000150),
                           mpf(0.00000000073)]))
        cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
        solar_anomaly = poly(c, [mpf(2.5534), (mpf(1236.85) * mpf(29.10535669)), mpf(-0.0000014), mpf(-0.00000011)])
        lunar_anomaly = poly(c, [mpf(201.5643), (mpf(385.81693528) * mpf(1236.85)), mpf(0.0107582), mpf(0.00001238), mpf(-0.000000058)])
        moon_argument = poly(c, [mpf(160.7108), (mpf(390.67050284) * mpf(1236.85)), mpf(-0.0016118), mpf(-0.00000227), mpf(0.000000011)])
        cap_omega = poly(c, [mpf(124.7746), (mpf(-1.56375588) * mpf(1236.85)), mpf(0.0020672), mpf(0.00000215)])
        E_factor = [0, 1, 0, 0, 1, 1, 2, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0]
        solar_coeff = [0, 1, 0, 0, -1, 1, 2, 0, 0, 1, 0, 1, 1, -1, 2,
                       0, 3, 1, 0, 1, -1, -1, 1, 0]
        lunar_coeff = [1, 0, 2, 0, 1, 1, 0, 1, 1, 2, 3, 0, 0, 2, 1, 2,
                       0, 1, 2, 1, 1, 1, 3, 4]
        moon_coeff = [0, 0, 0, 2, 0, 0, 0, -2, 2, 0, 0, 2, -2, 0, 0,
                      -2, 0, -2, 2, 2, 2, -2, 0, 0]
        sine_coeff = [mpf(-0.40720), mpf(0.17241), mpf(0.01608),
                      mpf(0.01039),  mpf(0.00739), mpf(-0.00514),
                      mpf(0.00208), mpf(-0.00111), mpf(-0.00057),
                      mpf(0.00056), mpf(-0.00042), mpf(0.00042),
                      mpf(0.00038), mpf(-0.00024), mpf(-0.00007),
                      mpf(0.00004), mpf(0.00004), mpf(0.00003),
                      mpf(0.00003), mpf(-0.00003), mpf(0.00003),
                      mpf(-0.00002), mpf(-0.00002), mpf(0.00002)]
        correction = ((mpf(-0.00017) * sin_degrees(cap_omega)) +
                      sigma([sine_coeff, E_factor, solar_coeff,
                             lunar_coeff, moon_coeff],
                            lambda v, w, x, y, z: (v *
                                        pow(cap_E, w) *
                                        sin_degrees((x * solar_anomaly) + 
                                                    (y * lunar_anomaly) +
                                                    (z * moon_argument)))))
        add_const = [mpf(251.88), mpf(251.83), mpf(349.42), mpf(84.66),
                     mpf(141.74), mpf(207.14), mpf(154.84), mpf(34.52),
                     mpf(207.19), mpf(291.34), mpf(161.72), mpf(239.56),
                     mpf(331.55)]
        add_coeff = [mpf(0.016321), mpf(26.651886), mpf(36.412478),
                     mpf(18.206239), mpf(53.303771), mpf(2.453732),
                     mpf(7.306860), mpf(27.261239), mpf(0.121824),
                     mpf(1.844379), mpf(24.198154), mpf(25.513099),
                     mpf(3.592518)]
        add_factor = [mpf(0.000165), mpf(0.000164), mpf(0.000126),
                      mpf(0.000110), mpf(0.000062), mpf(0.000060),
                      mpf(0.000056), mpf(0.000047), mpf(0.000042),
                      mpf(0.000040), mpf(0.000037), mpf(0.000035),
                      mpf(0.000023)]
        extra = (mpf(0.000325) * sin_degrees(poly(c, [mpf(299.77), mpf(132.8475848), mpf(-0.009173)])))
        additional = sigma([add_const, add_coeff, add_factor],
                           lambda i, j, l: l * sin_degrees(i + j * k))
    
        return cls.universal_from_dynamical(approx + correction + extra + additional)
    
    @classmethod
    def new_moon_before(cls, tee):
        """Return the moment UT of last new moon before moment tee."""
        t0 = cls.nth_new_moon(0)
        phi = cls.lunar_phase(tee)
        n = iround(((tee - t0) / cls.MEAN_SYNODIC_MONTH) - (phi / 360.0))
        return cls.nth_new_moon(final_int(n - 1, lambda k: cls.nth_new_moon(k) < tee))

    @classmethod    
    def new_moon_at_or_after(cls, tee):
        """Return the moment UT of first new moon at or after moment, tee."""
        t0 = cls.nth_new_moon(0)
        phi = cls.lunar_phase(tee)
        n = iround((tee - t0) / cls.MEAN_SYNODIC_MONTH - phi / 360.0)
        return cls.nth_new_moon(next_int(n, lambda k: cls.nth_new_moon(k) >= tee))
    
    @classmethod    
    def lunar_phase(cls, tee):
        """Return the lunar phase, as an angle in degrees, at moment tee.
        An angle of 0 means a new moon, 90 degrees means the
        first quarter, 180 means a full moon, and 270 degrees
        means the last quarter."""
        phi = mod(cls.lunar_longitude(tee) - cls.solar_longitude(tee), 360)
        t0 = cls.nth_new_moon(0)
        n = iround((tee - t0) / cls.MEAN_SYNODIC_MONTH)
        phi_prime = (360 *
                     mod((tee - cls.nth_new_moon(n)) / cls.MEAN_SYNODIC_MONTH, 1))
        if abs(phi - phi_prime) > 180:
            return phi_prime
        else:
            return phi
    
    @classmethod    
    def lunar_phase_at_or_before(cls, phi, tee):
        """Return the moment UT of the last time at or before moment, tee,
        when the lunar_phase was phi degrees."""
        tau = (tee -
               (cls.MEAN_SYNODIC_MONTH  *
                (1.0 / 360.0) *
                mod(cls.lunar_phase(tee) - phi, 360)))
        a = tau - 2
        b = min(tee, tau +2)
        return invert_angular(cls.lunar_phase, phi, a, b)

    @classmethod
    def visible_crescent(self, date):
        """Return S. K. Shaukat's criterion for likely
        visibility of crescent moon on eve of date 'date',
        at location 'location'."""
        tee = self.universal_from_standard(self.dusk(date - 1, mpf(4.5)))
        phase = self.lunar_phase(tee)
        altitude = self.lunar_altitude(tee)
        arc_of_light = arccos_degrees(cos_degrees(self.lunar_latitude(tee)) * cos_degrees(phase))
        return ((self.NEW < phase < self.FIRST_QUARTER) and
                (mpf(10.6) <= arc_of_light <= 90) and
                (altitude > mpf(4.1)))
    
    def phasis_on_or_before(self, date):
        """Return the closest fixed date on or before date 'date', when crescent
        moon first became visible at location 'location'."""
        mean = date - ifloor(self.lunar_phase(date + 1) / 360.0 * self.MEAN_SYNODIC_MONTH)
        tau = ((mean - 30)
               if (((date - mean) <= 3) and (not self.visible_crescent(date)))
               else (mean - 2))
        return  next_int(tau, lambda d: self.visible_crescent(d))

    @classmethod
    def lunar_phase_at_or_after(cls, phi, tee):
        """Return the moment UT of the next time at or after moment, tee,
        when the lunar_phase is phi degrees."""
        tau = (tee +
               (cls.MEAN_SYNODIC_MONTH    *
                (1.0 / 360.0) *
                mod(phi - cls.lunar_phase(tee), 360)))
        a = max(tee, tau - 2)
        b = tau + 2
        return invert_angular(cls.lunar_phase, phi, a, b)

    def lunar_altitude(self, tee):
        """Return the geocentric altitude of moon at moment, tee,
        at location, location, as a small positive/negative angle in degrees,
        ignoring parallax and refraction.  Adapted from 'Astronomical
        Algorithms' by Jean Meeus, Willmann_Bell, Inc., 1998."""
        lamb = self.lunar_longitude(tee)
        beta = self.lunar_latitude(tee)
        alpha = self.right_ascension(tee, beta, lamb)
        delta = self.declination(tee, beta, lamb)
        theta0 = self.sidereal_from_moment(tee)
        cap_H = mod(theta0 + self.longitude - alpha, 360)
        altitude = arcsin_degrees(
            (sin_degrees(self.latitude) * sin_degrees(delta)) +
            (cos_degrees(self.latitude) * cos_degrees(delta) * cos_degrees(cap_H)))
        return mod(altitude + 180, 360) - 180
     
    @classmethod
    def lunar_distance(cls, tee):
        """Return the distance to moon (in meters) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed."""
        c = cls.julian_centuries(tee)
        cap_D = cls.lunar_elongation(c)
        cap_M = cls.solar_anomaly(c)
        cap_M_prime = cls.lunar_anomaly(c)
        cap_F = cls.moon_node(c)
        cap_E = poly(c, [1, mpf(-0.002516), mpf(-0.0000074)])
        args_lunar_elongation = \
            [0, 2, 2, 0, 0, 0, 2, 2, 2, 2, 0, 1, 0, 2, 0, 0, 4, 0, 4, 2, 2, 1,
             1, 2, 2, 4, 2, 0, 2, 2, 1, 2, 0, 0, 2, 2, 2, 4, 0, 3, 2, 4, 0, 2,
             2, 2, 4, 0, 4, 1, 2, 0, 1, 3, 4, 2, 0, 1, 2, 2,]
        args_solar_anomaly = \
            [0, 0, 0, 0, 1, 0, 0, -1, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1,
             0, 1, -1, 0, 0, 0, 1, 0, -1, 0, -2, 1, 2, -2, 0, 0, -1, 0, 0, 1,
             -1, 2, 2, 1, -1, 0, 0, -1, 0, 1, 0, 1, 0, 0, -1, 2, 1, 0, 0]
        args_lunar_anomaly = \
            [1, -1, 0, 2, 0, 0, -2, -1, 1, 0, -1, 0, 1, 0, 1, 1, -1, 3, -2,
             -1, 0, -1, 0, 1, 2, 0, -3, -2, -1, -2, 1, 0, 2, 0, -1, 1, 0,
             -1, 2, -1, 1, -2, -1, -1, -2, 0, 1, 4, 0, -2, 0, 2, 1, -2, -3,
             2, 1, -1, 3, -1]
        args_moon_node = \
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, -2, 2, -2, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, -2, 2, 0, 2, 0, 0, 0, 0,
             0, 0, -2, 0, 0, 0, 0, -2, -2, 0, 0, 0, 0, 0, 0, 0, -2]
        cosine_coefficients = \
            [-20905355, -3699111, -2955968, -569925, 48888, -3149,
             246158, -152138, -170733, -204586, -129620, 108743,
             104755, 10321, 0, 79661, -34782, -23210, -21636, 24208,
             30824, -8379, -16675, -12831, -10445, -11650, 14403,
             -7003, 0, 10056, 6322, -9884, 5751, 0, -4950, 4130, 0,
             -3958, 0, 3258, 2616, -1897, -2117, 2354, 0, 0, -1423,
             -1117, -1571, -1739, 0, -4421, 0, 0, 0, 0, 1165, 0, 0,
             8752]
        correction = sigma ([cosine_coefficients,
                             args_lunar_elongation,
                             args_solar_anomaly,
                             args_lunar_anomaly,
                             args_moon_node],
                            lambda v, w, x, y, z: (v *
                                        pow(cap_E, abs(x)) * 
                                        cos_degrees((w * cap_D) +
                                                       (x * cap_M) +
                                                       (y * cap_M_prime) +
                                                       (z * cap_F))))
        return 385000560 + correction
    
    @classmethod
    def lunar_position(cls, tee):
        """Return the moon position (geocentric latitude and longitude [in degrees]
        and distance [in meters]) at moment, tee.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed."""
        return (cls.lunar_latitude(tee), cls.lunar_longitude(tee), cls.lunar_distance(tee))
    
    def lunar_parallax(self, tee):
        """Return the parallax of moon at moment, tee, at location, location.
        Adapted from "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 1998."""
        geo = self.lunar_altitude(tee)
        Delta = self.lunar_distance(tee)
        alt = 6378140 / Delta
        arg = alt * cos_degrees(geo)
        return arcsin_degrees(arg)
    
    def topocentric_lunar_altitude(self, tee):
        """Return the topocentric altitude of moon at moment, tee,
        at location, location, as a small positive/negative angle in degrees,
        ignoring refraction."""
        return self.lunar_altitude(tee) - self.lunar_parallax(tee)
    
    @classmethod
    def lunar_diameter(cls, tee):
        """Return the geocentric apparent lunar diameter of the moon (in
        degrees) at moment, tee.  Adapted from 'Astronomical
        Algorithms' by Jean Meeus, Willmann_Bell, Inc., 2nd ed."""
        return (1792367000/9) / cls.lunar_distance(tee)

MECCA = Location(angle(21, 25, 24), angle(39, 49, 24), 298, Clock.days_from_hours(3))
JERUSALEM = Location(31.8, 35.2, 800, Clock.days_from_hours(2))
BRUXELLES = Location(angle(4, 21, 17), angle(50, 50, 47), 800, Clock.days_from_hours(1))
URBANA = Location(40.1, -88.2, 225, Clock.days_from_hours(-6))
GREENWHICH = Location(51.4777815, 0, 46.9, Clock.days_from_hours(0))
