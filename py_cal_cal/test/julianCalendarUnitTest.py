# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable1TestCaseBase
class JulianSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            julian_from_fixed(self.testvalue), julian_date(1945, OCTOBER, 30))
        self.assertEqual(
            roman_from_fixed(self.testvalue),
            roman_date(1945, NOVEMBER, KALENDS, 3, is_julian_leap_year(1945)))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue,
                    fixed_from_julian(julian_date(1945, OCTOBER, 30)))
        self.assertEqual(
            self.testvalue,
            fixed_from_roman(roman_date(1945, NOVEMBER, KALENDS, 3,
                                        is_julian_leap_year(1945))))

    def testLeapYear(self):
        self.assertTrue(is_julian_leap_year(2000))
        self.assertTrue(is_julian_leap_year(1900))

class RomanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            roman_from_fixed(self.testvalue),
            roman_date(1945, NOVEMBER, KALENDS, 3, False))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue,
                    fixed_from_roman(roman_date(1945,
                                                NOVEMBER,
                                                KALENDS,
                                                3,
                                                False)))

class JulianDayAppendixCTestCase(AppendixCTable1TestCaseBase,
                                  unittest.TestCase):
    def testJulianDay(self):
        for i in range(len(self.rd)):
            # julian day
            self.assertEqual(jd_from_fixed(self.rd[i]), self.jd[i])
            self.assertEqual(fixed_from_jd(self.jd[i]), self.rd[i])
            # modified julian day
            self.assertEqual(mjd_from_fixed(self.rd[i]), self.mjd[i])
            self.assertEqual(fixed_from_mjd(self.mjd[i]), self.rd[i])



class JulianAppendixCTestCase(AppendixCTable1TestCaseBase):
    def testJulian(self):
        for i in range(len(self.rd)):
            # julian date
            self.assertEqual(julian_from_fixed(self.rd[i]), self.jdt[i])
            self.assertEqual(fixed_from_julian(self.jdt[i]), self.rd[i])
            # julian date, roman name
            self.assertEqual(roman_from_fixed(self.rd[i]), self.jrn[i])
            self.assertEqual(fixed_from_roman(self.jrn[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()


