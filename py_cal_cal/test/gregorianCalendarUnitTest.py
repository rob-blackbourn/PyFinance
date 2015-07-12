# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable1TestCaseBase
class GregorianCalendarSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
        self.aDate = gregorian_date(1945, NOVEMBER, 12)
        self.myDate = gregorian_date(1967, JANUARY, 30)
        self.aLeapDate = gregorian_date(1900, MARCH, 1)

    def testConversionFromFixed(self):
        self.assertEqual(
            gregorian_from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_gregorian(self.aDate))

    def testLeapYear(self):
        self.assertTrue(is_gregorian_leap_year(2000))
        self.assertTrue(not is_gregorian_leap_year(1900))

    def testDayNumber(self):
        self.assertEqual(day_number(self.myDate), 30)
        self.assertEqual(day_number(self.aLeapDate), 60)

class GregorianAppendixCTestCase(AppendixCTable1TestCaseBase,
                                  unittest.TestCase):
    def testGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                gregorian_year_from_fixed(self.rd[i]), standard_year(self.gd[i]))

    def testAltGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(alt_gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(alt_fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                alt_gregorian_year_from_fixed(self.rd[i]),
                standard_year(self.gd[i]))


if __name__ == "__main__":
    unittest.main()


