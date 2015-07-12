# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable3TestCaseBase


class EasterAppendixCTestCase(AppendixCTable3TestCaseBase,
                               unittest.TestCase):
    def testEaster(self):
        for i in range(len(self.rd)):
            self.assertEqual(
                 gregorian_from_fixed(orthodox_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.je[i])
            self.assertEqual(
                 gregorian_from_fixed(alt_orthodox_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.je[i])
            self.assertEqual(
                 gregorian_from_fixed(easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.ge[i])
            self.assertEqual(
                 gregorian_from_fixed(astronomical_easter(
                       gregorian_year_from_fixed(self.rd[i]))),
                 self.ae[i])


if __name__ == "__main__":
    unittest.main()


