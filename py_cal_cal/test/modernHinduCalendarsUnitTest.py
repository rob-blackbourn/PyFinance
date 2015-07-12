# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable4TestCaseBase

class ModernHinduAppendixCTestCase(AppendixCTable4TestCaseBase,
                                    unittest.TestCase):
    def testHinduSolarModernToFixed(self):
        for i in range(len(self.rd)):
            # hindu solar
            #    modern
            self.assertEqual(fixed_from_hindu_solar(self.mhs[i]), self.rd[i])

    def testHinduSolarModernFromFixed(self):
        for i in range(len(self.rd)):
            # hindu solar
            #    modern
            self.assertEqual(hindu_solar_from_fixed(self.rd[i]), self.mhs[i])

    def testHinduSolarAstronomicalToFixed(self):
        for i in range(len(self.rd)):
            #    astronomical
            self.assertEqual(fixed_from_astro_hindu_solar(self.ahs[i]), self.rd[i])

    def testHinduSolarAstronomicalFromFixed(self):
        for i in range(len(self.rd)):
            #    astronomical
            self.assertEqual(astro_hindu_solar_from_fixed(self.rd[i]), self.ahs[i])

    def testHinduLunisolarModernToFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    modern
            self.assertEqual(fixed_from_hindu_lunar(self.mhl[i]), self.rd[i])

    def testHinduLunisolarModernFromFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    modern
            self.assertEqual(hindu_lunar_from_fixed(self.rd[i]), self.mhl[i])

    def testHinduLunisolarAstronomicalToFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    astronomical
            self.assertEqual(fixed_from_astro_hindu_lunar(self.ahl[i]), self.rd[i])

    def testHinduLunisolarAstronomicalFromFixed(self):
        for i in range(len(self.rd)):
            # hindu lunisolar
            #    astronomical
            self.assertEqual(astro_hindu_lunar_from_fixed(self.rd[i]), self.ahl[i])


if __name__ == "__main__":
    unittest.main()



