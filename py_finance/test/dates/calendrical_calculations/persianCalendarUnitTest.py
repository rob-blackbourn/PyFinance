# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable3TestCaseBase

class PersianAppendixCTestCase(AppendixCTable3TestCaseBase,
                                unittest.TestCase):
    def testPersian(self):
        for i in range(len(self.rd)):
            # persian arithmetic
            self.assertEqual(
                fixed_from_arithmetic_persian(self.par[i]), self.rd[i])
            self.assertEqual(
                arithmetic_persian_from_fixed(self.rd[i]), self.par[i])
            # persian astronomical
            self.assertEqual(persian_from_fixed(self.rd[i]), self.pas[i])
            self.assertEqual(fixed_from_persian(self.pas[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()



