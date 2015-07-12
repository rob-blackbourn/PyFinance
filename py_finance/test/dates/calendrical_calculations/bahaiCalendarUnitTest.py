# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable2TestCaseBase

class BahaiAppendixCTestCase(AppendixCTable2TestCaseBase,
                              unittest.TestCase):
    def testBahai(self):
        for i in range(len(self.rd)):
            # bahai
            self.assertEqual(bahai_from_fixed(self.rd[i]), self.bd[i])
            self.assertEqual(fixed_from_bahai(self.bd[i]), self.rd[i])
            # bahai future
            self.assertEqual(future_bahai_from_fixed(self.rd[i]), self.bf[i])
            self.assertEqual(fixed_from_future_bahai(self.bf[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()



