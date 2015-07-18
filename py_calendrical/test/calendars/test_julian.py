import unittest

from py_calendrical.calendars.julian import JulianDate, JulianDay,\
    ModifiedJulianDay
from py_calendrical.calendars.gregorian import JulianMonth

class TestJulianDate(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(JulianDate.from_fixed(self.testvalue), JulianDate(1945, JulianMonth.October, 30))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, JulianDate(1945, JulianMonth.October, 30).to_fixed())

    def testLeapYear(self):
        self.assertTrue(JulianDate.is_leap_year(2000))
        self.assertTrue(JulianDate.is_leap_year(1900))

class TestJulianDay(unittest.TestCase):
    
    def testKnownDates(self):
        
        knownDates = {
            -214193 : 1507231.5,
            -61387  : 1660037.5,
            25469   : 1746893.5,
            49217   : 1770641.5,
            171307  : 1892731.5,
            210155  : 1931579.5,
            253427  : 1974851.5,
            369740  : 2091164.5,
            400085  : 2121509.5,
            434355  : 2155779.5,
            452605  : 2174029.5,
            470160  : 2191584.5,
            473837  : 2195261.5,
            507850  : 2229274.5,
            524156  : 2245580.5,
            544676  : 2266100.5,
            567118  : 2288542.5,
            569477  : 2290901.5,
            601716  : 2323140.5,
            613424  : 2334848.5,
            626596  : 2348020.5,
            645554  : 2366978.5,
            664224  : 2385648.5,
            671401  : 2392825.5,
            694799  : 2416223.5,
            704424  : 2425848.5,
            708842  : 2430266.5,
            709409  : 2430833.5,
            709580  : 2431004.5,
            727274  : 2448698.5,
            728714  : 2450138.5,
            744313  : 2465737.5,
            764652  : 2486076.5
        }

        for (fixed_date, julian_day) in knownDates.iteritems():
            self.assertEqual(fixed_date, JulianDay(julian_day).to_fixed(), "Convert julian day to fixed")
            self.assertEqual(julian_day, JulianDay.from_fixed(fixed_date).julian_day, "Convert fixed to Julian day")

class TestModifiedJulianDay(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193 : -892769,
            -61387 : -739963,
            25469  : -653107,
            49217  : -629359,
            171307 : -507269,
            210155 : -468421,
            253427 : -425149,
            369740 : -308836,
            400085 : -278491,
            434355 : -244221,
            452605 : -225971,
            470160 : -208416,
            473837 : -204739,
            507850 : -170726,
            524156 : -154420,
            544676 : -133900,
            567118 : -111458,
            569477 : -109099,
            601716 : -76860,
            613424 : -65152,
            626596 : -51980,
            645554 : -33022,
            664224 : -14352,
            671401 : -7175,
            694799 : 16223,
            704424 : 25848,
            708842 : 30266,
            709409 : 30833,
            709580 : 31004,
            727274 : 48698,
            728714 : 50138,
            744313 : 65737,
            764652 : 86076
        }

        for (fixed_date, modified_julian_day) in knownDates.iteritems():
            self.assertEqual(fixed_date, ModifiedJulianDay(modified_julian_day).to_fixed(), "Convert modified julian day to fixed")
            self.assertEqual(modified_julian_day, ModifiedJulianDay.from_fixed(fixed_date).modified_julian_day, "Convert fixed to modified julian day")
        
if __name__ == "__main__":
    unittest.main()