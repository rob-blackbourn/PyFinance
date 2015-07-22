import unittest

from py_calendrical.calendars.gregorian import GregorianDate
from py_calendrical.month_of_year import MonthOfYear

class TestGregorianCalendar(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347
        self.aDate = GregorianDate(1945, MonthOfYear.November, 12)
        self.myDate = GregorianDate(1967, MonthOfYear.January, 30)
        self.aLeapDate = GregorianDate(1900, MonthOfYear.March, 1)

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

    def testKnownDates(self):
        
        knownDates = {
            -214193 : GregorianDate(-586, 7, 24),
            -61387 : GregorianDate(-168, 12, 5),
            25469 : GregorianDate(70, 9, 24),
            49217 : GregorianDate(135, 10, 2),
            171307 : GregorianDate(470, 1, 8),
            210155 : GregorianDate(576, 5, 20),
            253427 : GregorianDate(694, 11, 10),
            369740 : GregorianDate(1013, 4, 25),
            400085 : GregorianDate(1096, 5, 24),
            434355 : GregorianDate(1190, 3, 23),
            452605 : GregorianDate(1240, 3, 10),
            470160 : GregorianDate(1288, 4, 2),
            473837 : GregorianDate(1298, 4, 27),
            507850 : GregorianDate(1391, 6, 12),
            524156 : GregorianDate(1436, 2, 3),
            544676 : GregorianDate(1492, 4, 9),
            567118 : GregorianDate(1553, 9, 19),
            569477 : GregorianDate(1560, 3, 5),
            601716 : GregorianDate(1648, 6, 10),
            613424 : GregorianDate(1680, 6, 30),
            626596 : GregorianDate(1716, 7, 24),
            645554 : GregorianDate(1768, 6, 19),
            664224 : GregorianDate(1819, 8, 2),
            671401 : GregorianDate(1839, 3, 27),
            694799 : GregorianDate(1903, 4, 19),
            704424 : GregorianDate(1929, 8, 25),
            708842 : GregorianDate(1941, 9, 29),
            709409 : GregorianDate(1943, 4, 19),
            709580 : GregorianDate(1943, 10, 7),
            727274 : GregorianDate(1992, 3, 17),
            728714 : GregorianDate(1996, 2, 25),
            744313 : GregorianDate(2038, 11, 10),
            764652 : GregorianDate(2094, 7, 18)
        }
        
        for (fixed_date, gregorian_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, gregorian_date.to_fixed(), "Convert to fixed")
            self.assertEqual(GregorianDate.from_fixed(fixed_date), gregorian_date, "Convert from fixed")

        
if __name__ == "__main__":
    unittest.main()