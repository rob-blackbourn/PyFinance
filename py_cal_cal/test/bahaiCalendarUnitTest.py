# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable2TestCaseBase

class BahaiAppendixCTestCase(AppendixCTable2TestCaseBase,
                              unittest.TestCase):
    def testBahai(self):
        for i in range(len(self.rd)):
            # bahai
            self.assertEqual(bahai_from_fixed(self.rd[i]), self.bd[i])
            self.assertEqual(fixed_from_bahai(self.bd[i]), self.rd[i])
            # bahai future
            self.assertEqual(from_future_fixed(self.rd[i]), self.bf[i])
            self.assertEqual(to_future_fixed(self.bf[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()



