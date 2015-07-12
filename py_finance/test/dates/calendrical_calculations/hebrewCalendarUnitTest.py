# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable3TestCaseBase
class HebrewSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            hebrew_from_fixed(self.testvalue), hebrew_date(5706, KISLEV, 7))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_hebrew(hebrew_date(5706, KISLEV, 7)))


class HebrewHolidaysTestCase(unittest.TestCase):
    def testBirkathHaHama(self):
        self.assertNotEqual(birkath_ha_hama(1925), [])
        self.assertEqual(birkath_ha_hama(1926), [])
        self.assertNotEqual(birkath_ha_hama(1925+28), [])

    def testTzomTevet(self):
        """test tzom tevet (Tevet 10): see page 104"""
        self.assertEqual(len(tzom_tevet(1982)), 2)
        self.assertEqual(len(tzom_tevet(1984)), 0)

    def testPossibleHebrewDays(self):
        """see page 110, Calendrical Calculations, 3rd edition."""
        self.assertEqual(set(possible_hebrew_days(SHEVAT, 15)),
                    set([THURSDAY, SATURDAY, MONDAY, TUESDAY, WEDNESDAY]))

class HebrewAppendixCTestCase(AppendixCTable3TestCaseBase,
                               unittest.TestCase):
    def testHebrew(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_hebrew(self.hd[i]), self.rd[i])
            self.assertEqual(hebrew_from_fixed(self.rd[i]), self.hd[i])
            # observational
            self.assertEqual(
                observational_hebrew_from_fixed(self.rd[i]), self.ho[i])
            self.assertEqual(
                fixed_from_observational_hebrew(self.ho[i]), self.rd[i])



if __name__ == "__main__":
    unittest.main()



