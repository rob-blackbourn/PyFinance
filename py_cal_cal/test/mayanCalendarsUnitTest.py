# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable2TestCaseBase
class MayanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(mayan_long_count_from_fixed(self.testvalue),
                         mayan_long_count_date(12, 16, 11, 16, 9))
        self.assertEqual(mayan_long_count_from_fixed(0),
                         mayan_long_count_date(7, 17, 18, 13, 2))
        self.assertEqual(mayan_haab_from_fixed(self.testvalue),
                         mayan_haab_date(11, 7))
        self.assertEqual(mayan_tzolkin_from_fixed(self.testvalue),
                         mayan_tzolkin_date(11, 9))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue,
            fixed_from_mayan_long_count(
                mayan_long_count_date(12, 16, 11, 16, 9)))
        self.assertEqual(
            rd(0),
            fixed_from_mayan_long_count(
                mayan_long_count_date(7, 17, 18, 13, 2)))
        self.assertEqual(mayan_haab_on_or_before(mayan_haab_date(11, 7), self.testvalue), self.testvalue)
        self.assertEqual(
            mayan_tzolkin_on_or_before(
                mayan_tzolkin_date(11, 9), self.testvalue),
            self.testvalue)

class AztecSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            aztec_xihuitl_from_fixed(self.testvalue),
            aztec_xihuitl_date(2, 1))

    def testConversionToFixed(self):
        self.assertEqual(
            aztec_xihuitl_on_or_before(
                aztec_xihuitl_date(2, 1), self.testvalue),
            self.testvalue)

class MayanAppendixCTestCase(AppendixCTable2TestCaseBase,
                              unittest.TestCase):
    def testMayan(self):
        for i in range(len(self.rd)):
            # mayan (long count)
            self.assertEqual(
                mayan_long_count_from_fixed(self.rd[i]), self.mlc[i])
            self.assertEqual(
                fixed_from_mayan_long_count(self.mlc[i]), self.rd[i])
            # mayan (haab)
            self.assertEqual(mayan_haab_from_fixed(self.rd[i]), self.mh[i])
            # mayan (tzolkin)
            self.assertEqual(mayan_tzolkin_from_fixed(self.rd[i]), self.mt[i])

    def testAztec(self):
        for i in range(len(self.rd)):
            # aztec xihuitl
            self.assertEqual(aztec_xihuitl_from_fixed(self.rd[i]), self.ax[i])
            # aztec tonalpohualli
            self.assertEqual(
                aztec_tonalpohualli_from_fixed(self.rd[i]), self.at[i])


if __name__ == "__main__":
    unittest.main()


