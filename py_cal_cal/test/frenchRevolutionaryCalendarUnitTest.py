# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable3TestCaseBase
def testMidnightInParis(self):
    d = fixed_from_gregorian(gregorian_date(1992,OCTOBER, 13)) 
    self.assertEqual(midnight_in_paris(d), d+1)



class FrenchRevolutionaryAppendixCTestCase(AppendixCTable3TestCaseBase,
                                            unittest.TestCase):
    #def assertEqual(one, two, msg=""):
    #    print one, two

    def testFrenchRevolutionary(self):
        for i in range(len(self.rd)):
            # french revolutionary original
            self.assertEqual(fixed_from_french(self.fr[i]), self.rd[i])
            self.assertEqual(french_from_fixed(self.rd[i]), self.fr[i])
            # french revolutionary modified
            self.assertEqual(fixed_from_arithmetic_french(self.frm[i]), self.rd[i])
            self.assertEqual(arithmetic_french_from_fixed(self.rd[i]), self.frm[i])

if __name__ == "__main__":
    unittest.main()



