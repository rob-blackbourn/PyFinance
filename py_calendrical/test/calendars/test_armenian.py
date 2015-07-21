import unittest

from py_calendrical.calendars.armenian import ArmenianDate

class ArmenianSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(ArmenianDate.from_fixed(self.testvalue), ArmenianDate(1395, 4, 5))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, ArmenianDate(1395, 4, 5).to_fixed())
    
    def testKnownDates(self):
        knownDates = {
            -214193: ArmenianDate(-1138, 4, 10),
            -61387: ArmenianDate(-720, 12, 6),
            25469: ArmenianDate(-482, 11, 22),
            49217: ArmenianDate(-417, 12, 15),
            171307: ArmenianDate(-82, 6, 10),
            210155: ArmenianDate(24, 11, 18),
            253427: ArmenianDate(143, 6, 5),
            369740: ArmenianDate(462, 2, 3),
            400085: ArmenianDate(545, 3, 23),
            434355: ArmenianDate(639, 2, 13),
            452605: ArmenianDate(689, 2, 13),
            470160: ArmenianDate(737, 3, 18),
            473837: ArmenianDate(747, 4, 15),
            507850: ArmenianDate(840, 6, 23),
            524156: ArmenianDate(885, 2, 24),
            544676: ArmenianDate(941, 5, 14),
            567118: ArmenianDate(1002, 11, 11),
            569477: ArmenianDate(1009, 4, 25),
            601716: ArmenianDate(1097, 8, 24),
            613424: ArmenianDate(1129, 9, 22),
            626596: ArmenianDate(1165, 10, 24),
            645554: ArmenianDate(1217, 10, 2),
            664224: ArmenianDate(1268, 11, 27),
            671401: ArmenianDate(1288, 7, 24),
            694799: ArmenianDate(1352, 9, 2),
            704424: ArmenianDate(1379, 1, 12),
            708842: ArmenianDate(1391, 2, 20),
            709409: ArmenianDate(1392, 9, 12),
            709580: ArmenianDate(1393, 2, 28),
            727274: ArmenianDate(1441, 8, 22),
            728714: ArmenianDate(1445, 8, 2),
            744313: ArmenianDate(1488, 4, 26),
            764652: ArmenianDate(1544, 1, 15)                       
        }
        
        for (fixed_date, armenian_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, armenian_date.to_fixed(), "Convert to fixed")
            self.assertEqual(ArmenianDate.from_fixed(fixed_date), armenian_date, "Convert from fixed")

if __name__ == "__main__":
    unittest.main()