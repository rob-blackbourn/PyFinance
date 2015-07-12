# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable3TestCaseBase
class BalineseSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            bali_pawukon_from_fixed(self.testvalue),
            balinese_date(True, 2, 1, 1, 3, 1, 2, 5, 7, 2))

    def testConversionToFixed(self):
        self.assertEqual(
            bali_on_or_before(
                balinese_date(True, 2, 1, 1, 3, 1, 2, 5, 7, 2),
                self.testvalue),
            self.testvalue)

class BalineseAppendixCTestCase(AppendixCTable3TestCaseBase):
    def testBalinese(self):
        for i in range(len(self.rd)):
            self.assertEqual(bali_pawukon_from_fixed(self.rd[i]), self.bd[i])


if __name__ == "__main__":
    unittest.main()


