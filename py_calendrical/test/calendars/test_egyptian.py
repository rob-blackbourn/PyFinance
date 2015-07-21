import unittest

from py_calendrical.calendars.egyptian import EgyptianDate

class EgyptianSmokeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347
        self.aDate = EgyptianDate(2694, 7, 10)

    def testConversionFromFixed(self):
        self.assertEqual(EgyptianDate.from_fixed(self.testvalue), EgyptianDate(2694, 7, 10))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, EgyptianDate(2694, 7, 10).to_fixed())

    def testKnownDates(self):
        knownDates = {
            -214193: EgyptianDate(161, 7, 15),
            -61387: EgyptianDate(580, 3, 6),
            25469: EgyptianDate(818, 2, 22),
            49217: EgyptianDate(883, 3, 15),
            171307: EgyptianDate(1217, 9, 15),
            210155: EgyptianDate(1324, 2, 18),
            253427: EgyptianDate(1442, 9, 10),
            369740: EgyptianDate(1761, 5, 8),
            400085: EgyptianDate(1844, 6, 28),
            434355: EgyptianDate(1938, 5, 18),
            452605: EgyptianDate(1988, 5, 18),
            470160: EgyptianDate(2036, 6, 23),
            473837: EgyptianDate(2046, 7, 20),
            507850: EgyptianDate(2139, 9, 28),
            524156: EgyptianDate(2184, 5, 29),
            544676: EgyptianDate(2240, 8, 19),
            567118: EgyptianDate(2302, 2, 11),
            569477: EgyptianDate(2308, 7, 30),
            601716: EgyptianDate(2396, 11, 29),
            613424: EgyptianDate(2428, 12, 27),
            626596: EgyptianDate(2465, 1, 24),
            645554: EgyptianDate(2517, 1, 2),
            664224: EgyptianDate(2568, 2, 27),
            671401: EgyptianDate(2587, 10, 29),
            694799: EgyptianDate(2651, 12, 7),
            704424: EgyptianDate(2678, 4, 17),
            708842: EgyptianDate(2690, 5, 25),
            709409: EgyptianDate(2691, 12, 17),
            709580: EgyptianDate(2692, 6, 3),
            727274: EgyptianDate(2740, 11, 27),
            728714: EgyptianDate(2744, 11, 7),
            744313: EgyptianDate(2787, 8, 1),
            764652: EgyptianDate(2843, 4, 20)                     
        }
        
        for (fixed_date, egyptian_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, egyptian_date.to_fixed(), "Convert to fixed")
            self.assertEqual(EgyptianDate.from_fixed(fixed_date), egyptian_date, "Convert from fixed")

if __name__ == "__main__":
    unittest.main()