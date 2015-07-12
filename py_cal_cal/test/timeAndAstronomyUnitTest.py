# AUTOMATICALLY GENERATED FROM pycalcal.nw: ANY CHANGES WILL BE OVERWRITTEN.

from py_cal_cal.pycalcal import *
import unittest

from py_cal_cal.test.appendixCUnitTest import AppendixCTable5TestCaseBase
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


if __name__ == "__main__":
    unittest.main()



