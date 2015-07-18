import unittest

from py_calendrical.calendars.iso import IsoDate

class ISOSmokeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347
        self.aDate = IsoDate(1945, 46, 1)

    def testConversionFromFixed(self):
        self.assertEqual(IsoDate.from_fixed(self.testvalue), IsoDate(1945, 46, 1))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, IsoDate(1945, 46, 1).to_fixed())

    def testKnownDates(self):
        knownDates = {
            -214193: IsoDate(-586, 29, 7),
            -61387: IsoDate(-168, 49, 3),
            25469: IsoDate(70, 39, 3),
            49217: IsoDate(135, 39, 7),
            171307: IsoDate(470, 2, 3),
            210155: IsoDate(576, 21, 1),
            253427: IsoDate(694, 45, 6),
            369740: IsoDate(1013, 16, 7),
            400085: IsoDate(1096, 21, 7),
            434355: IsoDate(1190, 12, 5),
            452605: IsoDate(1240, 10, 6),
            470160: IsoDate(1288, 14, 5),
            473837: IsoDate(1298, 17, 7),
            507850: IsoDate(1391, 23, 7),
            524156: IsoDate(1436, 5, 3),
            544676: IsoDate(1492, 14, 6),
            567118: IsoDate(1553, 38, 6),
            569477: IsoDate(1560, 9, 6),
            601716: IsoDate(1648, 24, 3),
            613424: IsoDate(1680, 26, 7),
            626596: IsoDate(1716, 30, 5),
            645554: IsoDate(1768, 24, 7),
            664224: IsoDate(1819, 31, 1),
            671401: IsoDate(1839, 13, 3),
            694799: IsoDate(1903, 16, 7),
            704424: IsoDate(1929, 34, 7),
            708842: IsoDate(1941, 40, 1),
            709409: IsoDate(1943, 16, 1),
            709580: IsoDate(1943, 40, 4),
            727274: IsoDate(1992, 12, 2),
            728714: IsoDate(1996, 8, 7),
            744313: IsoDate(2038, 45, 3),
            764652: IsoDate(2094, 28, 7)
        }
    
        for (fixed_date, iso_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, iso_date.to_fixed(), "Convert to fixed")
            self.assertEqual(IsoDate.from_fixed(fixed_date), iso_date, "Convert from fixed")
    
if __name__ == "__main__":
    unittest.main()