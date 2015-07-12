# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable2TestCaseBase
class IslamicSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            islamic_from_fixed(self.testvalue), islamic_date(1364, 12, 6))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_islamic(islamic_date(1364, 12, 6)))

class IslamicAppendixCTestCase(AppendixCTable2TestCaseBase,
                                unittest.TestCase):
    def testIslamic(self):
        for i in range(len(self.rd)):
            # islamic
            self.assertEqual(islamic_from_fixed(self.rd[i]), self.id[i])
            self.assertEqual(fixed_from_islamic(self.id[i]), self.rd[i])
            # islamic (observational)
            self.assertEqual(
                fixed_from_observational_islamic(self.io[i]), self.rd[i])
            self.assertEqual(
                observational_islamic_from_fixed(self.rd[i]), self.io[i])


if __name__ == "__main__":
    unittest.main()



