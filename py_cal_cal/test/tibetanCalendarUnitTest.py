# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable4TestCaseBase

class TibetanAppendixCTestCase(AppendixCTable4TestCaseBase, unittest.TestCase):
    def testTibetan(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_tibetan(self.td[i]), self.rd[i])
            self.assertEqual(tibetan_from_fixed(self.rd[i]), self.td[i])



if __name__ == "__main__":
    unittest.main()



