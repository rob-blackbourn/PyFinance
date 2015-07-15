from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.triganometry import sin_degrees, normalized_degrees 
from py_calendrical.py_cal_cal import poly, sigma, invert_angular
from py_calendrical.astro import Astro

class Solar(Astro):
   
    MEAN_TROPICAL_YEAR = mpf(365.242189)
 
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
    def estimate_prior_solar_longitude(cls, lam, tee):
        """Return approximate moment at or before tee
        when solar longitude just exceeded lam degrees."""
        rate = cls.MEAN_TROPICAL_YEAR / 360.0
        tau = tee - (rate * mod(cls.solar_longitude(tee) - lam, 360))
        cap_Delta = mod(cls.solar_longitude(tau) - lam + 180, 360) - 180
        return min(tee, tau - (rate * cap_Delta))
    
    @classmethod
    def solar_anomaly(cls, c):
        """Return mean anomaly of sun (in degrees) at moment
        given in Julian centuries c.
        Adapted from eq. 47.3 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(357.5291092), mpf(35999.0502909), mpf(-0.0001536), mpf(1.0/24490000.0)]))

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
        rate = cls.MEAN_TROPICAL_YEAR / 360
        tau = tee + rate * mod(lam - cls.solar_longitude(tee), 360)
        a = max(tee, tau - 5)
        b = tau + 5
        return invert_angular(cls.solar_longitude, lam, a, b)
