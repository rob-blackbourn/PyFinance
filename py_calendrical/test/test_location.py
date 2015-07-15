import unittest

from mpmath import mpf

from py_calendrical.calendars.gregorian import GregorianDate, JulianMonth
from py_calendrical.time_arithmatic import Clock
from py_calendrical.location import Location
from py_calendrical.py_cal_cal import iround
from py_calendrical.calendars.hebrew import JAFFA
from py_calendrical.astro import Astro
from py_calendrical.lunar import Lunar
from py_calendrical.solar import Solar

class TestLocation(unittest.TestCase):

    def testUniversalFromDynamical(self):
        date = GregorianDate(1977, JulianMonth.February, 18)
        time = Clock(3, 37, 40).to_time()
        td   = date.to_fixed() + time 
        utc  = Astro.universal_from_dynamical(td)
        clk  = Clock.from_moment(utc)
        self.assertEqual(clk.hour, 3)
        self.assertEqual(clk.minute, 36)
        self.assertEqual(iround(clk.second), 52)
        
    def testDynamicalFromUniversal(self):
        date = GregorianDate(1977, JulianMonth.February, 18)
        time = Clock(3, 36, 52).to_time()
        utc  = date.to_fixed() + time 
        td   = Astro.dynamical_from_universal(utc)
        clk  = Clock.from_moment(td)
        self.assertEqual(clk.hour, 3)
        self.assertEqual(clk.minute, 37)
        self.assertEqual(iround(clk.second), 40)

        date = GregorianDate(333, JulianMonth.February, 6)
        time = Clock(6, 0, 0).to_time()
        utc  = date.to_fixed() + time 
        td   = Astro.dynamical_from_universal(utc)
        clk  = Clock.from_moment(td)
        self.assertEqual(clk.hour, 7)
        self.assertEqual(clk.minute, 57)
        self.assertAlmostEqual(clk.second, 54.66054, 4)

    def testNutation(self):
        TD  = GregorianDate(1992, JulianMonth.April, 12).to_fixed()
        tee = Astro.universal_from_dynamical(TD)
        self.assertAlmostEqual(Astro.nutation(tee), mpf(0.004610), 3)

    def testMeanLunarLongitude(self):
        self.assertAlmostEqual(Lunar.mean_lunar_longitude(-0.077221081451), 134.290182, 6)

    def testLunarElongation(self):
        self.assertAlmostEqual(Lunar.lunar_elongation(-0.077221081451), 113.842304, 6)

    def testSolarAnomaly(self):
        self.assertAlmostEqual(Solar.solar_anomaly(-0.077221081451), 97.643514, 6)

    def testLunarAnomaly(self):
        self.assertAlmostEqual(Lunar.lunar_anomaly(-0.077221081451), 5.150833, 6)

    def testMoonNode(self):
        self.assertAlmostEqual(Lunar.moon_node(-0.077221081451), 219.889721, 6)

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
            lamb = Lunar.lunar_longitude(self.rd[i])
            beta = Lunar.lunar_latitude(self.rd[i])
            alpha = Astro.declination(self.rd[i], beta, lamb)
            self.assertAlmostEqual(alpha, self.declinations[i], 7)

    def testRightAscension(self):
        for i in range(len(self.rd)):
            lamb = Lunar.lunar_longitude(self.rd[i])
            beta = Lunar.lunar_latitude(self.rd[i])
            alpha = Astro.right_ascension(self.rd[i], beta, lamb)
            self.assertAlmostEqual(alpha, self.right_ascensions[i], 7)

    def testLunarAltitude(self):
        for i in range(len(self.rd)):
            alpha = JAFFA.lunar_altitude(self.rd[i])
            self.assertAlmostEqual(alpha, self.lunar_altitudes[i], 6)

    def testDusk(self):
        for i in range(len(self.rd)):
            du = JAFFA.dusk(self.rd[i] - 1, mpf(4.5))
            self.assertAlmostEqual(du, self.dusks[i], 0)

if __name__ == "__main__":
    unittest.main()