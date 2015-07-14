import unittest

from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.gregorian import JulianMonth
from py_calendrical.calendars.roman import RomanDate, Event

class RomanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(RomanDate.from_fixed(self.testvalue), RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, RomanDate(1945, JulianMonth.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)).to_fixed())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()