# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable1TestCaseBase
from appendixCUnitTest import AppendixCTable2TestCaseBase
class CopticSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            coptic_from_fixed(self.testvalue), coptic_date(1662, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_coptic(coptic_date(1662, 3, 3)))


class EthiopicSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            ethiopic_from_fixed(self.testvalue), ethiopic_date(1938, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_ethiopic(ethiopic_date(1938, 3, 3)))

class CopticAppendixCTestCase(AppendixCTable1TestCaseBase):
    def testCoptic(self):
        for i in range(len(self.rd)):
            self.assertEqual(coptic_from_fixed(self.rd[i]), self.cd[i])
            self.assertEqual(fixed_from_coptic(self.cd[i]), self.rd[i])



class EthiopicAppendixCTestCase(AppendixCTable2TestCaseBase,
                                 unittest.TestCase):
    def testEthiopic(self):
        for i in range(len(self.rd)):
            # ethiopic day
            self.assertEqual(ethiopic_from_fixed(self.rd[i]), self.ed[i])
            self.assertEqual(fixed_from_ethiopic(self.ed[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()


