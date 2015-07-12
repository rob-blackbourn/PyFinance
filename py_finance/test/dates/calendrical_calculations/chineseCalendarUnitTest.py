# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable4TestCaseBase
#############################################
# Tests other than the ones from Appendix C #
#############################################

class ChineseAppendixCTestCase(AppendixCTable4TestCaseBase,
                                unittest.TestCase):
    def testChinese(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_chinese(self.cd[i]), self.rd[i])
            self.assertEqual(chinese_from_fixed(self.rd[i]), self.cd[i])
            self.assertEqual(chinese_day_name(self.rd[i]), self.cn[i])
            self.assertAlmostEqual(
                major_solar_term_on_or_after(self.rd[i]), self.ms[i], 6)


if __name__ == "__main__":
    unittest.main()



