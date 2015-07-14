import unittest

from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth

class GregorianCalendarSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347
        self.aDate = GregorianDate(1945, JulianMonth.November, 12)
        self.myDate = GregorianDate(1967, JulianMonth.January, 30)
        self.aLeapDate = GregorianDate(1900, JulianMonth.March, 1)

    def testConversionFromFixed(self):
        self.assertEqual(GregorianDate.from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, self.aDate.to_fixed())

    def testLeapYear(self):
        self.assertTrue(GregorianDate.is_leap_year(2000))
        self.assertFalse(GregorianDate.is_leap_year(1900))

    def testDayNumber(self):
        self.assertEqual(self.myDate.day_number(), 30)
        self.assertEqual(self.aLeapDate.day_number(), 60)


if __name__ == "__main__":
    unittest.main()