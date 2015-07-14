import unittest

from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.gregorian import JulianMonth

class JulianSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(JulianDate.from_fixed(self.testvalue), JulianDate(1945, JulianMonth.October, 30))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, JulianDate(1945, JulianMonth.October, 30).to_fixed())

    def testLeapYear(self):
        self.assertTrue(JulianDate.is_leap_year(2000))
        self.assertTrue(JulianDate.is_leap_year(1900))

if __name__ == "__main__":
    unittest.main()