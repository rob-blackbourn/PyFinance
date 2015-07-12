# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable4TestCaseBase
class OldHinduSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            old_hindu_solar_from_fixed(self.testvalue),
            hindu_solar_date(5046, 7, 29))
        self.assertEqual(
            old_hindu_lunar_from_fixed(self.testvalue),
            old_hindu_lunar_date(5046, 8, False, 8))
        # FIXME (not sure the check is correct)
        self.assertEqual(jovian_year(self.testvalue), 32)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue,
            fixed_from_old_hindu_solar(hindu_solar_date(5046, 7, 29)))
        self.assertEqual(
            self.testvalue,
            fixed_from_old_hindu_lunar(
                old_hindu_lunar_date(5046, 8, False, 8)))

class OldHinduAppendixCTestCase(AppendixCTable4TestCaseBase,
                                 unittest.TestCase):
    def testOldHindu(self):
        for i in range(len(self.rd)):
            # solar
            self.assertEqual(fixed_from_old_hindu_solar(self.ohs[i]), self.rd[i])
            self.assertEqual(old_hindu_solar_from_fixed(self.rd[i]), self.ohs[i])
            # lunisolar
            self.assertEqual(fixed_from_old_hindu_lunar(self.ohl[i]), self.rd[i])
            self.assertEqual(old_hindu_lunar_from_fixed(self.rd[i]), self.ohl[i])



if __name__ == "__main__":
    unittest.main()


