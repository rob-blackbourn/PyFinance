# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable1TestCaseBase
class ISOSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
        self.aDate = iso_date(1945, 46, 1)

    def testConversionFromFixed(self):
        self.assertEqual(
            iso_from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_iso(self.aDate))

class IsoAppendixCTestCase(AppendixCTable1TestCaseBase, unittest.TestCase):
    def testIso(self):
        for i in range(len(self.rd)):
            self.assertEqual(iso_from_fixed(self.rd[i]), self.isod[i])
            self.assertEqual(fixed_from_iso(self.isod[i]), self.rd[i])


if __name__ == "__main__":
    unittest.main()



