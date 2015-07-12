# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_finance.dates.calendrical_calculations.pycalcal import *
import unittest

from appendixCUnitTest import AppendixCTable1TestCaseBase
class BasicCodeTestCase(unittest.TestCase):
    def testNext(self):
        self.assertEqual(next(0, lambda i: i == 3), 3)
        self.assertEqual(next(0, lambda i: i == 0), 0)



    def testFinal(self):
        self.assertEqual(final(0, lambda i: i == 3), -1)
        self.assertEqual(final(0, lambda i: i < 3), 2)
        self.assertEqual(final(0, lambda i: i < 0), -1)


    def testSumma(self):
        self.assertEqual(summa(lambda x: 1, 1, lambda i: i<=4), 4)
        self.assertEqual(summa(lambda x: 1, 0, lambda i: i>=4), 0)
        self.assertEqual(summa(lambda x: x**2, 1, lambda i: i<=4), 30)

    def testAltSumma(self):
        # I should add more tests with floating point arithmetic...
        self.assertEqual(altsumma(lambda x: 1.0, 1, lambda i: i<=4), 4)
        self.assertEqual(altsumma(lambda x: 1.0, 0, lambda i: i>=4), 0)
        self.assertEqual(altsumma(lambda x: x**2, 1, lambda i: i<=4), 30)


    def testBinarySearch(self):
        fminusy = lambda x, y: fx(x) - y
        p = lambda a, b: abs(fminusy(0.5 * (a+b), y)) <= 10**-5
        e = lambda x: fminusy(x, y) >= 0
        #  function y = f(x), f(x) = x, y0 = 1.0; solution is x0 = 1.0
        fx = lambda x: x
        y  = 1.0
        x0 = 1.0
        self.assertTrue(binary_search(0.0, 3.1, p, e) - x0 <= 10 ** -5)
        # new function y = f(x), f(x) = x**2 - 4*x + 4, y0 = 0.0; solution x0=2.0
        y = 0.0
        x0 = 2.0
        fx = lambda x: x**2 -4 * x + 4.0
        self.assertTrue(binary_search(1.5, 2.5, p, e) - x0 <= 10 ** -5)



    def testInvertAngular(self):
        from math import tan, radians
        # find angle theta such that tan(theta) = 1
        # assert that theta - pi/4 <= 10**-5
        self.assertTrue(invert_angular(tan,
                                    1.0,
                                    0,
                                    radians(60.0)) - radians(45.0) <= 10**-5)


    def testSigma(self):
        a = [ 1, 2, 3, 4]
        b = [ 5, 6, 7, 8]
        c = [ 9,10,11,12]
        ell = [a,b,c]
        bi  = lambda x, y, z: x * y * z
        self.assertEqual(sigma(ell, bi), 780)



    def testPoly(self):
        self.assertEqual(poly(0, [2, 2, 1]), 2)
        self.assertEqual(poly(1, [2, 2, 1]), 5)



    def testClockFromMoment(self):
        c = clock_from_moment(3.5)
        self.assertEqual(hour(c), 12)
        self.assertEqual(minute(c), 0)
        self.assertAlmostEqual(seconds(c), 0, 2)
        
        c = clock_from_moment(3.75)
        self.assertEqual(hour(c), 18)
        self.assertEqual(minute(c), 0)
        self.assertAlmostEqual(seconds(c), 0, 2)
        
        c = clock_from_moment(3.8)
        self.assertEqual(hour(c), 19)
        self.assertEqual(minute(c), 11)
        self.assertAlmostEqual(seconds(c), 59.9999, 2)



    def testTimeFromClock(self):
        self.assertAlmostEqual(time_from_clock([12, 0, 0]), 0.5, 2)
        self.assertAlmostEqual(time_from_clock([18, 0, 0]), 0.75, 2)
        self.assertAlmostEqual(time_from_clock([19, 12, 0]), 0.8, 2)




class BasicAppendixCTestCase(AppendixCTable1TestCaseBase, unittest.TestCase):
    def testWeekdays(self):
        for i in range(len(self.rd)):
            # weekdays
            self.assertEqual(day_of_week_from_fixed(self.rd[i]), self.wd[i])


if __name__ == "__main__":
    unittest.main()
