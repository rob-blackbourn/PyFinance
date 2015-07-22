import unittest

from py_calendrical.calendars.julian import JulianDate
from py_calendrical.calendars.roman import RomanDate, Event
from py_calendrical.month_of_year import MonthOfYear

class RomanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
 
    def testConversionFromFixed(self):
        self.assertEqual(RomanDate.from_fixed(self.testvalue), RomanDate(1945, MonthOfYear.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)))
 
    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, RomanDate(1945, MonthOfYear.November, Event.Kalends, 3, JulianDate.is_leap_year(1945)).to_fixed())

    def testComparisons(self):
        a1 = RomanDate(1945, MonthOfYear.November, Event.Kalends, 3, JulianDate.is_leap_year(1945))
        a2 = RomanDate(1945, MonthOfYear.November, Event.Kalends, 3, JulianDate.is_leap_year(1945))
        b = RomanDate(1945, MonthOfYear.November, Event.Kalends, 4, JulianDate.is_leap_year(1945))
        self.assertEqual(a1, a2, "Should be equal")
        self.assertTrue(a1 < b, "Should be less")
    
    def testKnownDates(self):
        knownDates = {
            -214193: RomanDate(-587, 8, Event.Kalends, 3, False),
            -61387: RomanDate(-169, 12, Event.Ides, 6, False),
            25469: RomanDate(70, 10, Event.Kalends, 6, False),
            49217: RomanDate(135, 10, Event.Nones, 5, False),
            171307: RomanDate(470, 1, Event.Ides, 7, False),
            210155: RomanDate(576, 6, Event.Kalends, 15, False),
            253427: RomanDate(694, 11, Event.Ides, 7, False),
            369740: RomanDate(1013, 5, Event.Kalends, 13, False),
            400085: RomanDate(1096, 6, Event.Kalends, 15, False),
            434355: RomanDate(1190, 4, Event.Kalends, 17, False),
            452605: RomanDate(1240, 3, Event.Nones, 5, False),
            470160: RomanDate(1288, 4, Event.Kalends, 7, False),
            473837: RomanDate(1298, 5, Event.Kalends, 12, False),
            507850: RomanDate(1391, 6, Event.Nones, 2, False),
            524156: RomanDate(1436, 2, Event.Kalends, 8, False),
            544676: RomanDate(1492, 4, Event.Kalends, 2, False),
            567118: RomanDate(1553, 9, Event.Ides, 5, False),
            569477: RomanDate(1560, 3, Event.Kalends, 6, False),
            601716: RomanDate(1648, 6, Event.Kalends, 2, False),
            613424: RomanDate(1680, 7, Event.Kalends, 12, False),
            626596: RomanDate(1716, 7, Event.Ides, 3, False),
            645554: RomanDate(1768, 6, Event.Ides, 6, False),
            664224: RomanDate(1819, 8, Event.Kalends, 12, False),
            671401: RomanDate(1839, 3, Event.Ides, 1, False),
            694799: RomanDate(1903, 4, Event.Ides, 8, False),
            704424: RomanDate(1929, 8, Event.Ides, 2, False),
            708842: RomanDate(1941, 10, Event.Kalends, 16, False),
            709409: RomanDate(1943, 4, Event.Ides, 8, False),
            709580: RomanDate(1943, 10, Event.Kalends, 8, False),
            727274: RomanDate(1992, 3, Event.Nones, 4, False),
            728714: RomanDate(1996, 2, Event.Ides, 2, False),
            744313: RomanDate(2038, 11, Event.Kalends, 5, False),
            764652: RomanDate(2094, 7, Event.Nones, 3, False)
        }
        for (fixed_date, roman_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, roman_date.to_fixed(), "Convert to fixed")
            self.assertEqual(RomanDate.from_fixed(fixed_date), roman_date, "Convert from fixed")
        
if __name__ == "__main__":
    unittest.main()
