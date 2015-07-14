import unittest

from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.gregorian import JulianMonth
from py_calendrical.calendars.roman import RomanDate, Event
from py_calendrical.utils import reduce_cond

class RomanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
 
    def testConversionFromFixed(self):
        self.assertEqual(RomanDate.from_fixed(self.testvalue), RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)))
 
    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)).to_fixed())

    def testComparisons(self):
        a1 = RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945))
        a2 = RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945))
        b = RomanDate(1945, JulianMonth.November, Event.Kalends, 4, JulianDate.is_leap_year(1945))
        self.assertEqual(a1, a2, "Should be equal")
        self.assertTrue(a1 < b, "Should be less")
        
if __name__ == "__main__":
    unittest.main()
