from __future__ import division
from operator import mod
from mpmath import mpf
from py_calendrical.triganometry import sin_degrees, cos_degrees, normalized_degrees 
from py_calendrical.py_cal_cal import iround, poly, sigma, invert_angular
from py_calendrical.utils import next_int, final_int
from py_calendrical.astro import Astro
from py_calendrical.solar import Solar

class Lunar(Astro):
    
    MEAN_SYNODIC_MONTH = mpf(29.530588861)
        
    NEW = 0
    FIRST_QUARTER = 90
    FULL = 180
    LAST_QUARTER = 270

    @classmethod
    def mean_lunar_longitude(cls, c):
        """Return mean longitude of moon (in degrees) at moment
        given in Julian centuries c (including the constant term of the
        effect of the light-time (-0".70).
        Adapted from eq. 47.1 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(218.3164477), mpf(481267.88123421),
                                   mpf(-0.0015786), mpf(1 / 538841.0),
                                   mpf(-1.0 / 65194000.0)]))
    
    @classmethod
    def lunar_elongation(cls, c):
        """Return elongation of moon (in degrees) at moment
        given in Julian centuries c.
        Adapted from eq. 47.2 in "Astronomical Algorithms" by Jean Meeus,
        Willmann_Bell, Inc., 2nd ed. with corrections, 2005."""
        return normalized_degrees(poly(c, [mpf(297.8501921), mpf(445267.1114034),
                                    mpf(-0.0018819), mpf(1/545868),
                                    mpf(-1/113065000)]))
    
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
        cap_M = Solar.solar_anomaly(c)
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
        venus = ((3958/1000000) * sin_degrees(A1))
        A2 = mpf(53.09) + c * mpf(479264.29)
        jupiter = ((318/1000000) * sin_degrees(A2))
        flat_earth = ((1962/1000000) * sin_degrees(cap_L_prime - cap_F))
    
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
        cap_M = Solar.solar_anomaly(c)
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
        venus = ((175/1000000) *
                 (sin_degrees(mpf(119.75) + c * mpf(131.849) + cap_F) +
                  sin_degrees(mpf(119.75) + c * mpf(131.849) - cap_F)))
        flat_earth = ((-2235/1000000) *  sin_degrees(cap_L_prime) +
                      (127/1000000) * sin_degrees(cap_L_prime - cap_M_prime) +
                      (-115/1000000) * sin_degrees(cap_L_prime + cap_M_prime))
        extra = ((382/1000000) *
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
        n = iround(((tee - t0) / cls.MEAN_SYNODIC_MONTH) - (phi / 360))
        return cls.nth_new_moon(final_int(n - 1, lambda k: cls.nth_new_moon(k) < tee))

    @classmethod    
    def new_moon_at_or_after(cls, tee):
        """Return the moment UT of first new moon at or after moment, tee."""
        t0 = cls.nth_new_moon(0)
        phi = cls.lunar_phase(tee)
        n = iround((tee - t0) / cls.MEAN_SYNODIC_MONTH - phi / 360)
        return cls.nth_new_moon(next_int(n, lambda k: cls.nth_new_moon(k) >= tee))
    
    @classmethod    
    def lunar_phase(cls, tee):
        """Return the lunar phase, as an angle in degrees, at moment tee.
        An angle of 0 means a new moon, 90 degrees means the
        first quarter, 180 means a full moon, and 270 degrees
        means the last quarter."""
        phi = mod(cls.lunar_longitude(tee) - Solar.solar_longitude(tee), 360)
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
                (1/360) *
                mod(cls.lunar_phase(tee) - phi, 360)))
        a = tau - 2
        b = min(tee, tau +2)
        return invert_angular(cls.lunar_phase, phi, a, b)

    @classmethod
    def lunar_phase_at_or_after(cls, phi, tee):
        """Return the moment UT of the next time at or after moment, tee,
        when the lunar_phase is phi degrees."""
        tau = (tee +
               (cls.MEAN_SYNODIC_MONTH    *
                (1/360) *
                mod(phi - cls.lunar_phase(tee), 360)))
        a = max(tee, tau - 2)
        b = tau + 2
        return invert_angular(cls.lunar_phase, phi, a, b)
     
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
    
    @classmethod
    def lunar_diameter(cls, tee):
        """Return the geocentric apparent lunar diameter of the moon (in
        degrees) at moment, tee.  Adapted from 'Astronomical
        Algorithms' by Jean Meeus, Willmann_Bell, Inc., 2nd ed."""
        return (1792367000/9) / cls.lunar_distance(tee)
