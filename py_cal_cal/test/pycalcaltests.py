# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

# Copyright (c) 2009 Enrico Spinielli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from py_cal_cal.pycalcal import *
from py_cal_cal.test.appendixCUnitTest import AppendixCTable1TestCaseBase
from py_cal_cal.test.appendixCUnitTest import AppendixCTable2TestCaseBase
from py_cal_cal.test.appendixCUnitTest import AppendixCTable3TestCaseBase
from py_cal_cal.test.appendixCUnitTest import AppendixCTable4TestCaseBase
from py_cal_cal.test.appendixCUnitTest import AppendixCTable5TestCaseBase
import unittest

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



class GregorianCalendarSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347
        self.aDate = gregorian_date(1945, NOVEMBER, 12)
        self.myDate = gregorian_date(1967, JANUARY, 30)
        self.aLeapDate = gregorian_date(1900, MARCH, 1)

    def testConversionFromFixed(self):
        self.assertEqual(
            gregorian_from_fixed(self.testvalue), self.aDate)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_gregorian(self.aDate))

    def testLeapYear(self):
        self.assertTrue(is_gregorian_leap_year(2000))
        self.assertTrue(not is_gregorian_leap_year(1900))

    def testDayNumber(self):
        self.assertEqual(day_number(self.myDate), 30)
        self.assertEqual(day_number(self.aLeapDate), 60)

class GregorianAppendixCTestCase(AppendixCTable1TestCaseBase,
                                  unittest.TestCase):
    def testGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                gregorian_year_from_fixed(self.rd[i]), standard_year(self.gd[i]))

    def testAltGregorian(self):
        for i in range(len(self.rd)):
            self.assertEqual(alt_gregorian_from_fixed(self.rd[i]), self.gd[i])
            self.assertEqual(alt_fixed_from_gregorian(self.gd[i]), self.rd[i])
            self.assertEqual(
                alt_gregorian_year_from_fixed(self.rd[i]),
                standard_year(self.gd[i]))


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


class JulianSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            julian_from_fixed(self.testvalue), julian_date(1945, OCTOBER, 30))
        self.assertEqual(
            roman_from_fixed(self.testvalue),
            roman_date(1945, NOVEMBER, KALENDS, 3, is_julian_leap_year(1945)))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue,
                    fixed_from_julian(julian_date(1945, OCTOBER, 30)))
        self.assertEqual(
            self.testvalue,
            fixed_from_roman(roman_date(1945, NOVEMBER, KALENDS, 3,
                                        is_julian_leap_year(1945))))

    def testLeapYear(self):
        self.assertTrue(is_julian_leap_year(2000))
        self.assertTrue(is_julian_leap_year(1900))

class RomanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            roman_from_fixed(self.testvalue),
            roman_date(1945, NOVEMBER, KALENDS, 3, False))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue,
                    fixed_from_roman(roman_date(1945,
                                                NOVEMBER,
                                                KALENDS,
                                                3,
                                                False)))

class JulianDayAppendixCTestCase(AppendixCTable1TestCaseBase,
                                  unittest.TestCase):
    def testJulianDay(self):
        for i in range(len(self.rd)):
            # julian day
            self.assertEqual(jd_from_fixed(self.rd[i]), self.jd[i])
            self.assertEqual(fixed_from_jd(self.jd[i]), self.rd[i])
            # modified julian day
            self.assertEqual(mjd_from_fixed(self.rd[i]), self.mjd[i])
            self.assertEqual(fixed_from_mjd(self.mjd[i]), self.rd[i])



class JulianAppendixCTestCase(AppendixCTable1TestCaseBase):
    def testJulian(self):
        for i in range(len(self.rd)):
            # julian date
            self.assertEqual(julian_from_fixed(self.rd[i]), self.jdt[i])
            self.assertEqual(fixed_from_julian(self.jdt[i]), self.rd[i])
            # julian date, roman name
            self.assertEqual(roman_from_fixed(self.rd[i]), self.jrn[i])
            self.assertEqual(fixed_from_roman(self.jrn[i]), self.rd[i])


class CopticSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            coptic_from_fixed(self.testvalue), coptic_date(1662, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_coptic(coptic_date(1662, 3, 3)))


class EthiopicSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            ethiopic_from_fixed(self.testvalue), ethiopic_date(1938, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_ethiopic(ethiopic_date(1938, 3, 3)))

class CopticAppendixCTestCase(AppendixCTable1TestCaseBase):
    def testCoptic(self):
        for i in range(len(self.rd)):
            self.assertEqual(coptic_from_fixed(self.rd[i]), self.cd[i])
            self.assertEqual(fixed_from_coptic(self.cd[i]), self.rd[i])



class EthiopicAppendixCTestCase(AppendixCTable2TestCaseBase,
                                 unittest.TestCase):
    def testEthiopic(self):
        for i in range(len(self.rd)):
            # ethiopic day
            self.assertEqual(ethiopic_from_fixed(self.rd[i]), self.ed[i])
            self.assertEqual(fixed_from_ethiopic(self.ed[i]), self.rd[i])




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


class IslamicSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            islamic_from_fixed(self.testvalue), islamic_date(1364, 12, 6))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_islamic(islamic_date(1364, 12, 6)))

class IslamicAppendixCTestCase(AppendixCTable2TestCaseBase,
                                unittest.TestCase):
    def testIslamic(self):
        for i in range(len(self.rd)):
            # islamic
            self.assertEqual(islamic_from_fixed(self.rd[i]), self.id[i])
            self.assertEqual(fixed_from_islamic(self.id[i]), self.rd[i])
            # islamic (observational)
            self.assertEqual(
                fixed_from_observational_islamic(self.io[i]), self.rd[i])
            self.assertEqual(
                observational_islamic_from_fixed(self.rd[i]), self.io[i])


class HebrewSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            hebrew_from_fixed(self.testvalue), hebrew_date(5706, KISLEV, 7))

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue, fixed_from_hebrew(hebrew_date(5706, KISLEV, 7)))


class HebrewHolidaysTestCase(unittest.TestCase):
    def testBirkathHaHama(self):
        self.assertNotEqual(birkath_ha_hama(1925), [])
        self.assertEqual(birkath_ha_hama(1926), [])
        self.assertNotEqual(birkath_ha_hama(1925+28), [])

    def testTzomTevet(self):
        """test tzom tevet (Tevet 10): see page 104"""
        self.assertEqual(len(tzom_tevet(1982)), 2)
        self.assertEqual(len(tzom_tevet(1984)), 0)

    def testPossibleHebrewDays(self):
        """see page 110, Calendrical Calculations, 3rd edition."""
        self.assertEqual(set(possible_hebrew_days(SHEVAT, 15)),
                    set([THURSDAY, SATURDAY, MONDAY, TUESDAY, WEDNESDAY]))

class HebrewAppendixCTestCase(AppendixCTable3TestCaseBase,
                               unittest.TestCase):
    def testHebrew(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_hebrew(self.hd[i]), self.rd[i])
            self.assertEqual(hebrew_from_fixed(self.rd[i]), self.hd[i])
            # observational
            self.assertEqual(
                observational_hebrew_from_fixed(self.rd[i]), self.ho[i])
            self.assertEqual(
                fixed_from_observational_hebrew(self.ho[i]), self.rd[i])



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
        self.assertEqual(
            mayan_haab_on_or_before(mayan_haab_date(11, 7), self.testvalue),
            self.testvalue)
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


class OldHinduSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            old_hindu_solar_from_fixed(self.testvalue),
            hindu_solar_date(5046, 7, 29))
        self.assertEqual(
            old_hindu_lunar_from_fixed(self.testvalue),
            old_hindu_lunar_date(5046, 8, False, 8))
        # FIXME (not sure the check is correct)
        self.assertEqual(jovian_year(self.testvalue), 32)

    def testConversionToFixed(self):
        self.assertEqual(
            self.testvalue,
            fixed_from_old_hindu_solar(hindu_solar_date(5046, 7, 29)))
        self.assertEqual(
            self.testvalue,
            fixed_from_old_hindu_lunar(
                old_hindu_lunar_date(5046, 8, False, 8)))

class OldHinduAppendixCTestCase(AppendixCTable4TestCaseBase,
                                 unittest.TestCase):
    def testOldHindu(self):
        for i in range(len(self.rd)):
            # solar
            self.assertEqual(fixed_from_old_hindu_solar(self.ohs[i]), self.rd[i])
            self.assertEqual(old_hindu_solar_from_fixed(self.rd[i]), self.ohs[i])
            # lunisolar
            self.assertEqual(fixed_from_old_hindu_lunar(self.ohl[i]), self.rd[i])
            self.assertEqual(old_hindu_lunar_from_fixed(self.rd[i]), self.ohl[i])



class BalineseSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(
            bali_pawukon_from_fixed(self.testvalue),
            balinese_date(True, 2, 1, 1, 3, 1, 2, 5, 7, 2))

    def testConversionToFixed(self):
        self.assertEqual(
            bali_on_or_before(
                balinese_date(True, 2, 1, 1, 3, 1, 2, 5, 7, 2),
                self.testvalue),
            self.testvalue)

class BalineseAppendixCTestCase(AppendixCTable3TestCaseBase):
    def testBalinese(self):
        for i in range(len(self.rd)):
            self.assertEqual(bali_pawukon_from_fixed(self.rd[i]), self.bd[i])


class TimeAndAstronomySmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.rd = [-214193, -61387, 25469, 49217, 171307, 210155, 253427,
                    369740, 400085, 434355, 452605, 470160, 473837, 507850,
                    524156, 544676, 567118, 569477, 601716, 613424, 626596,
                    645554, 664224, 671401, 694799, 704424, 708842, 709409,
                    709580, 727274, 728714, 744313, 764652]

        self.declinations = [341.009933681, 344.223866057, 344.349150723,
                             343.080796014, 6.111045686, 23.282088850,
                             11.054626067, 20.772095601, 350.530615797,
                             26.524557874, 24.624220236, 341.329137381,
                             22.952455871, 28.356788216, 11.708349719,
                             17.836387256, 1.234462343, 342.613034686,
                             339.494416096, 10.077195527, 356.273352051,
                             10.933004147, 333.162727246, 12.857424363,
                             342.981182734, 8.352097710, 342.717593219,
                             359.480653210, 339.868605556, 6.747953072,
                             15.403930316, 5.935073706, 6.502803786]

        self.right_ascensions = [243.344057675, 204.985406451, 210.404938685,
                                 292.982801046, 157.347243474, 109.710580543,
                                 38.206587532, 99.237553669, 334.622772431,
                                 92.594013257, 77.002562902, 275.265641321,
                                 132.240141523, 89.495057657, 21.938682002,
                                 51.336108524, 189.141475514, 323.504045205,
                                 317.763636501, 146.668234288, 183.868193626,
                                 143.441024476, 251.771505962, 154.432825924,
                                 288.759213491, 24.368877399, 291.218608152,
                                 190.563965149, 285.912816020, 152.814362172,
                                 50.014265486, 26.456502208, 177.918419842]

        self.lunar_altitudes = [-11.580406490, -13.996642398, -72.405467670,
                                 -26.949751162, 60.491536818, -32.333449636,
                                 43.325012802, -28.913935286, 20.844069354,
                                 -9.603298107, -13.290409748, 20.650429381,
                                 -9.068998404, -24.960604514, -34.865669400,
                                 -40.121041983, -50.193172697, -39.456259107,
                                 32.614203610, -46.078519304, -51.828340409,
                                 -42.577971851, -15.990046584, 28.658077283,
                                 22.718206310, 61.618573945, -26.504789606,
                                 32.371736207, -38.544325288, 31.594345546,
                                 -28.348377620, 30.478724056, -43.754783219]

        self.dusks = [-214193.22, -61387.297, 25468.746, 49216.734,
                       171306.7, 210154.78, 253426.7, 369739.78,
                       400084.8, 434354.78, 452604.75, 470159.78,
                       473836.78, 507849.8, 524155.75, 544675.7,
                       567117.7, 569476.7, 601715.75, 613423.75,
                       626595.75, 645553.75, 664223.75, 671400.7,
                       694798.75, 704423.75, 708841.7, 709408.75,
                       709579.7, 727273.7, 728713.7, 744312.7,
                       764651.75]


    def testDeclination(self):
        for i in range(len(self.rd)):
            lamb = lunar_longitude(self.rd[i])
            beta = lunar_latitude(self.rd[i])
            alpha = declination(self.rd[i], beta, lamb)
            self.assertAlmostEqual(alpha, self.declinations[i], 7)

    def testRightAscension(self):
        for i in range(len(self.rd)):
            lamb = lunar_longitude(self.rd[i])
            beta = lunar_latitude(self.rd[i])
            alpha = right_ascension(self.rd[i], beta, lamb)
            self.assertAlmostEqual(alpha, self.right_ascensions[i], 7)

    def testLunarAltitude(self):
        for i in range(len(self.rd)):
            alpha = lunar_altitude(self.rd[i], JAFFA)
            self.assertAlmostEqual(alpha, self.lunar_altitudes[i], 6)

    def testDusk(self):
        for i in range(len(self.rd)):
            du = dusk(self.rd[i] - 1, JAFFA, deg(mpf(4.5)))
            self.assertAlmostEqual(du, self.dusks[i], 0)


class AstronomicalAlgorithmsTestCase(unittest.TestCase):
    def testEclipticalFromEquatorial(self):
        # from the values in the Ch 13 Astronomical Algorithms
        ra, de = equatorial_from_ecliptical(113.215630, 6.684170, 23.4392911)
        self.assertAlmostEqual(ra, 116.328942, 5)
        self.assertAlmostEqual(de, 28.026183, 6)


    def testEquatorialFromEcliptical(self):
        # from the values in the Ch 13 Astronomical Algorithms
        lo, la = ecliptical_from_equatorial(116.328942, 28.026183, 23.4392911)
        self.assertAlmostEqual(lo, mpf(113.215630), 6)
        self.assertAlmostEqual(la,   mpf(6.684170), 6)


    def testHorizontalFromEquatorial(self):
        # from the values in the Ch 13 Astronomical Algorithms
        A, h = horizontal_from_equatorial(64.352133, -6.719892, angle(38, 55, 17))
        self.assertAlmostEqual(A, 68.0337, 4)
        self.assertAlmostEqual(h, 15.1249, 4)


    def testEquatorialFromHorizontal(self):
        # from the values in the Ch 13 Astronomical Algorithms
        H, d = equatorial_from_horizontal(68.0337, 15.1249, angle(38, 55, 17))
        self.assertAlmostEqual(H, 64.352133, 4)
        self.assertAlmostEqual(d, normalized_degrees(angle(-6,-43,-11.61)), 4)


    def testUrbanaWinter(self):
        # from the values in the book pag 191
        self.assertAlmostEqual(
            urbana_winter(2000), 730475.31751, 5)





class AstronomyAppendixCTestCase(AppendixCTable5TestCaseBase,
                                  unittest.TestCase):
    def testSolarLongitude(self):
        for i in range(len(self.rd)):
            # +0.5 takes into account that the value has to be
            # calculated at 12:00 UTC
            self.assertAlmostEqual(solar_longitude(self.rd[i] + 0.5),
                                   self.sl[i],
                                   6)

    def testNextSolsticeEquinox(self):
        # I run some tests for Gregorian year 1995 about new Moon and
        # start of season against data from HM Observatory...and they
        # are ok
        for i in range(len(self.rd)):
            t = [solar_longitude_after(SPRING, self.rd[i]),
                 solar_longitude_after(SUMMER, self.rd[i]),
                 solar_longitude_after(AUTUMN, self.rd[i]),
                 solar_longitude_after(WINTER, self.rd[i])]
            self.assertAlmostEqual(min(t), self.nse[i], 6)

    def testLunarLongitude(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(lunar_longitude(self.rd[i]),
                                   self.ll[i],
                                   6)

    def testNextNewMoon(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(new_moon_at_or_after(self.rd[i]),
                                   self.nnm[i],
                                   6)

    def testDawnInParis(self):
        # as clarified by Prof. Reingold in CL it is:
        #    (dawn day paris 18d0)
        # note that d0 stands for double float precision and in
        # the Python routines we use mpf with 52 digits for dawn()
        alpha = angle(18, 0, 0)
        for i in range(len(self.rd)):
            if (self.dip[i] == BOGUS):
                self.assertEqual(dawn(self.rd[i], PARIS, alpha), self.dip[i])
            else:
                self.assertAlmostEqual(
                           mod(dawn(self.rd[i], PARIS, alpha), 1),
                           mpf(self.dip[i]),
                           6)

    def testSunsetInJerusalem(self):
        for i in range(len(self.rd)):
            self.assertAlmostEqual(
                 mod(sunset(self.rd[i], JERUSALEM), 1),
                 float(self.sij[i]),
                 6)



class PersianAppendixCTestCase(AppendixCTable3TestCaseBase,
                                unittest.TestCase):
    def testPersian(self):
        for i in range(len(self.rd)):
            # persian arithmetic
            self.assertEqual(
                fixed_from_arithmetic_persian(self.par[i]), self.rd[i])
            self.assertEqual(
                arithmetic_persian_from_fixed(self.rd[i]), self.par[i])
            # persian astronomical
            self.assertEqual(persian_from_fixed(self.rd[i]), self.pas[i])
            self.assertEqual(fixed_from_persian(self.pas[i]), self.rd[i])



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



class TibetanAppendixCTestCase(AppendixCTable4TestCaseBase, unittest.TestCase):
    def testTibetan(self):
        for i in range(len(self.rd)):
            self.assertEqual(fixed_from_tibetan(self.td[i]), self.rd[i])
            self.assertEqual(tibetan_from_fixed(self.rd[i]), self.td[i])



class AstronomicalLunarCalendarsTestCase(unittest.TestCase):
    def testUniversalFromDynamical(self):
        # from Meeus Example 10.a, pag 78
        date = gregorian_date(1977, FEBRUARY, 18)
        time = time_from_clock([3, 37, 40])
        td   = fixed_from_gregorian(date) + time 
        utc  = universal_from_dynamical(td)
        clk  = clock_from_moment(utc)
        self.assertEqual(hour(clk), 3)
        self.assertEqual(minute(clk), 36)
        self.assertEqual(iround(seconds(clk)), 52)

    def testDynamicalFromUniversal(self):
        # from Meeus Example 10.a, pag 78 (well, inverse of)
        date = gregorian_date(1977, FEBRUARY, 18)
        time = time_from_clock([3, 36, 52])
        utc  = fixed_from_gregorian(date) + time 
        td   = dynamical_from_universal(utc)
        clk  = clock_from_moment(td)
        self.assertEqual(hour(clk), 3)
        self.assertEqual(minute(clk), 37)
        self.assertEqual(iround(seconds(clk)), 40)
        # from Meeus Example 10.b, pag 79
        # I shoud get 7:42 but I get [7, 57, mpf('54.660540372133255')]
        # The equivalent CL
        #     (load "calendrica-3.0.cl")
        #     (in-package "CC3")
        #     (setq date (gregorian-date 333 february  6))
        #     (setq time (time-from-clock '(6 0 0)))
        #     (setq utc (+ (fixed-from-gregorian date) time))
        #     (setq td (dynamical-from-universal utc))
        #     (setq clk (clock-from-moment td))
        # gives (7 57 54.660540566742383817L0) on CLisp on PC
        # The reply from Prof Reingold and Dershowitz says:
        # From      Ed Reingold <reingold@emr.cs.iit.edu>
        # To        Enrico Spinielli <enrico.spinielli@googlemail.com>
        # Cc        nachumd@tau.ac.il
        # date      Thu, Aug 6, 2009 at 3:46 PM
        # subject   Re: dynamical-from-universal values differ from Meeus
        # mailed-by emr.cs.iit.edu
        # hide details Aug 6
        # Our value of the ephemeris correction closely matches the value
        # given on the NASA web site
        # http://eclipse.gsfc.nasa.gov/SEhelp/deltat2004.html for 333
        # (interpolating between the years 300 and 400), namely,
        # their value is 7027 seconds, while ours is 7075 seconds.
        # Meeus uses 6146 seconds, the difference amounts to about 14 minutes.
        # With Allegro Common Lisp, our functions
        #
        # (clock-from-moment (dynamical-from-universal
        #                      (+ (fixed-from-julian '(333 2 6)) 0.25L0)))
        #
        # give
        #
        #      (7 57 54.660540372133255d0)
        #
        # while CLisp on my PC gives
        #
        #      (7 57 54.660540566742383817L0)
        #
        # The difference in Delta-T explains Meeus's value of 7:42am.
        #
        # I then follow Calendrica Calculations (and NASA)
        date = gregorian_date(333, FEBRUARY, 6)
        time = time_from_clock([6, 0, 0])
        utc  = fixed_from_gregorian(date) + time 
        td   = dynamical_from_universal(utc)
        clk  = clock_from_moment(td)
        self.assertEqual(hour(clk), 7)
        self.assertEqual(minute(clk), 57)
        self.assertAlmostEqual(seconds(clk), 54.66054, 4)


    def testNutation(self):
        # from Meeus, pag 343
        TD  = fixed_from_gregorian(gregorian_date(1992, APRIL, 12))
        tee = universal_from_dynamical(TD)
        self.assertAlmostEqual(nutation(tee), mpf(0.004610), 3)

    def testMeanLunarLongitude(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(mean_lunar_longitude(-0.077221081451), 134.290182, 6)

    def testLunarElongation(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(lunar_elongation(-0.077221081451), 113.842304, 6)

    def testSolarAnomaly(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(solar_anomaly(-0.077221081451), 97.643514, 6)


    def testLunarAnomaly(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(lunar_anomaly(-0.077221081451), 5.150833, 6)


    def testMoonNode(self):
        # from Example 47.a in Jan Meeus "Astronomical Algorithms" pag 342
        self.assertAlmostEqual(moon_node(-0.077221081451), 219.889721, 6)




if __name__ == "__main__":
    unittest.main()


