import unittest

from mpmath import mpf

from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.time_arithmatic import Clock
from py_calendrical.location import Location
from py_calendrical.py_cal_cal import iround

class TestLocation(unittest.TestCase):

    def testUniversalFromDynamical(self):
        date = GregorianDate(1977, JulianMonth.February, 18)
        time = Clock(3, 37, 40).to_time()
        td   = date.to_fixed() + time 
        utc  = Location.universal_from_dynamical(td)
        clk  = Clock.from_moment(utc)
        self.assertEqual(clk.hour, 3)
        self.assertEqual(clk.minute, 36)
        self.assertEqual(iround(clk.second), 52)
        
    def testDynamicalFromUniversal(self):
        date = GregorianDate(1977, JulianMonth.February, 18)
        time = Clock(3, 36, 52).to_time()
        utc  = date.to_fixed() + time 
        td   = Location.dynamical_from_universal(utc)
        clk  = Clock.from_moment(td)
        self.assertEqual(clk.hour, 3)
        self.assertEqual(clk.minute, 37)
        self.assertEqual(iround(clk.second), 40)

        date = GregorianDate(333, JulianMonth.February, 6)
        time = Clock(6, 0, 0).to_time()
        utc  = date.to_fixed() + time 
        td   = Location.dynamical_from_universal(utc)
        clk  = Clock.from_moment(td)
        self.assertEqual(clk.hour, 7)
        self.assertEqual(clk.minute, 57)
        self.assertAlmostEqual(clk.second, 54.66054, 4)

    def testNutation(self):
        TD  = GregorianDate(1992, JulianMonth.April, 12).to_fixed()
        tee = Location.universal_from_dynamical(TD)
        self.assertAlmostEqual(Location.nutation(tee), mpf(0.004610), 3)

    def testMeanLunarLongitude(self):
        self.assertAlmostEqual(Location.mean_lunar_longitude(-0.077221081451), 134.290182, 6)

    def testLunarElongation(self):
        self.assertAlmostEqual(Location.lunar_elongation(-0.077221081451), 113.842304, 6)

    def testSolarAnomaly(self):
        self.assertAlmostEqual(Location.solar_anomaly(-0.077221081451), 97.643514, 6)

    def testLunarAnomaly(self):
        self.assertAlmostEqual(Location.lunar_anomaly(-0.077221081451), 5.150833, 6)

    def testMoonNode(self):
        self.assertAlmostEqual(Location.moon_node(-0.077221081451), 219.889721, 6)

if __name__ == "__main__":
    unittest.main()