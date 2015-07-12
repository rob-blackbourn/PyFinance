# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable1TestCaseBase
class EgyptianSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
        self.aDate = egyptian_date(2694, 7, 10)

    def testConversionFromFixed(self):
        self.assertEqual(
            egyptian_from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_egyptian(self.aDate))

###############################
class ArmenianSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
        self.aDate = armenian_date(1395, 4, 5)

    def testConversionFromFixed(self):
        self.assertEqual(
            armenian_from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_armenian(self.aDate))

class ArmeniamAppendixCTestCase(AppendixCTable1TestCaseBase):
   def testArmenian(self):
       for i in range(len(self.rd)):
           self.assertEqual(armenian_from_fixed(self.rd[i]), self.ad[i])
           self.assertEqual(fixed_from_armenian(self.ad[i]), self.rd[i])



class EgyptianAppendixCTestCase(AppendixCTable1TestCaseBase):
   def testEgyptian(self):
       for i in range(len(self.rd)):
           self.assertEqual(egyptian_from_fixed(self.rd[i]), self.ed[i])
           self.assertEqual(fixed_from_egyptian(self.ed[i]), self.rd[i])



if __name__ == "__main__":
    unittest.main()


