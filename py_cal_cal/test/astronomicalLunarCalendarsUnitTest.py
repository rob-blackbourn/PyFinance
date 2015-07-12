# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable5TestCaseBase
class AstronomicalLunarCalendarsTestCase(unittest.TestCase):
    def testUniversalFromDynamical(self):
        # from Meeus Example 10.a, pag 78
        date = gregorian_date(1977, FEBRUARY, 18)
        time = time_from_clock([3, 37, 40])
        td   = fixed_from_gregorian(date) + time 
        utc  = universal_from_dynamical(td)
        clk  = clock_from_moment(utc)
        self.assertEqual(hour(clk), 3)
        self.assertEqual(minute(clk), 36)
        self.assertEqual(iround(seconds(clk)), 52)

    def testDynamicalFromUniversal(self):
        # from Meeus Example 10.a, pag 78 (well, inverse of)
        date = gregorian_date(1977, FEBRUARY, 18)
        time = time_from_clock([3, 36, 52])
        utc  = fixed_from_gregorian(date) + time 
        td   = dynamical_from_universal(utc)
        clk  = clock_from_moment(td)
        self.assertEqual(hour(clk), 3)
        self.assertEqual(minute(clk), 37)
        self.assertEqual(iround(seconds(clk)), 40)
        # from Meeus Example 10.b, pag 79
        # I shoud get 7:42 but I get [7, 57, mpf('54.660540372133255')]
        # The equivalent CL
        #     (load "calendrica-3.0.cl")
        #     (in-package "CC3")
        #     (setq date (gregorian-date 333 february  6))
        #     (setq time (time-from-clock '(6 0 0)))
        #     (setq utc (+ (fixed-from-gregorian date) time))
        #     (setq td (dynamical-from-universal utc))
        #     (setq clk (clock-from-moment td))
        # gives (7 57 54.660540566742383817L0) on CLisp on PC
        # The reply from Prof Reingold and Dershowitz says:
        # From      Ed Reingold <reingold@emr.cs.iit.edu>
        # To        Enrico Spinielli <enrico.spinielli@googlemail.com>
        # Cc        nachumd@tau.ac.il
        # date      Thu, Aug 6, 2009 at 3:46 PM
        # subject   Re: dynamical-from-universal values differ from Meeus
        # mailed-by emr.cs.iit.edu
        # hide details Aug 6
        # Our value of the ephemeris correction closely matches the value
        # given on the NASA web site
        # http://eclipse.gsfc.nasa.gov/SEhelp/deltat2004.html for 333
        # (interpolating between the years 300 and 400), namely,
        # their value is 7027 seconds, while ours is 7075 seconds.
        # Meeus uses 6146 seconds, the difference amounts to about 14 minutes.
        # With Allegro Common Lisp, our functions
        #
        # (clock-from-moment (dynamical-from-universal
        #                      (+ (fixed-from-julian '(333 2 6)) 0.25L0)))
        #
        # give
        #
        #      (7 57 54.660540372133255d0)
        #
        # while CLisp on my PC gives
        #
        #      (7 57 54.660540566742383817L0)
        #
        # The difference in Delta-T explains Meeus's value of 7:42am.
        #
        # I then follow Calendrica Calculations (and NASA)
        date = gregorian_date(333, FEBRUARY, 6)
        time = time_from_clock([6, 0, 0])
        utc  = fixed_from_gregorian(date) + time 
        td   = dynamical_from_universal(utc)
        clk  = clock_from_moment(td)
        self.assertEqual(hour(clk), 7)
        self.assertEqual(minute(clk), 57)
        self.assertAlmostEqual(seconds(clk), 54.66054, 4)


    def testNutation(self):
        # from Meeus, pag 343
        TD  = fixed_from_gregorian(gregorian_date(1992, APRIL, 12))
        tee = universal_from_dynamical(TD)
        self.assertAlmostEqual(nutation(tee), mpf(0.004610), 3)

    def testMeanLunarLongitude(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(mean_lunar_longitude(-0.077221081451), 134.290182, 6)

    def testLunarElongation(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(lunar_elongation(-0.077221081451), 113.842304, 6)

    def testSolarAnomaly(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(solar_anomaly(-0.077221081451), 97.643514, 6)


    def testLunarAnomaly(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(lunar_anomaly(-0.077221081451), 5.150833, 6)


    def testMoonNode(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(moon_node(-0.077221081451), 219.889721, 6)



if __name__ == "__main__":
    unittest.main()


