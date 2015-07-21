import unittest

from py_calendrical.calendars.coptic import CopticDate

class CopticSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(CopticDate.from_fixed(self.testvalue), CopticDate(1662, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, CopticDate(1662, 3, 3).to_fixed())

    def testKnownDates(self):
        knownDates = {
            -214193: CopticDate(-870, 12, 6),
            -61387: CopticDate(-451, 4, 12),
            25469: CopticDate(-213, 1, 29),
            49217: CopticDate(-148, 2, 5),
            171307: CopticDate(186, 5, 12),
            210155: CopticDate(292, 9, 23),
            253427: CopticDate(411, 3, 11),
            369740: CopticDate(729, 8, 24),
            400085: CopticDate(812, 9, 23),
            434355: CopticDate(906, 7, 20),
            452605: CopticDate(956, 7, 7),
            470160: CopticDate(1004, 7, 30),
            473837: CopticDate(1014, 8, 25),
            507850: CopticDate(1107, 10, 10),
            524156: CopticDate(1152, 5, 29),
            544676: CopticDate(1208, 8, 5),
            567118: CopticDate(1270, 1, 12),
            569477: CopticDate(1276, 6, 29),
            601716: CopticDate(1364, 10, 6),
            613424: CopticDate(1396, 10, 26),
            626596: CopticDate(1432, 11, 19),
            645554: CopticDate(1484, 10, 14),
            664224: CopticDate(1535, 11, 27),
            671401: CopticDate(1555, 7, 19),
            694799: CopticDate(1619, 8, 11),
            704424: CopticDate(1645, 12, 19),
            708842: CopticDate(1658, 1, 19),
            709409: CopticDate(1659, 8, 11),
            709580: CopticDate(1660, 1, 26),
            727274: CopticDate(1708, 7, 8),
            728714: CopticDate(1712, 6, 17),
            744313: CopticDate(1755, 3, 1),
            764652: CopticDate(1810, 11, 11)                      
        }
        
        for (fixed_date, coptic_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, coptic_date.to_fixed(), "Convert to fixed")
            self.assertEqual(CopticDate.from_fixed(fixed_date), coptic_date, "Convert from fixed")
        
if __name__ == "__main__":
    unittest.main()