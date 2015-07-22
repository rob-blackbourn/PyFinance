import unittest

from py_calendrical.calendars.hebrew import HebrewDate, HebrewMonth,\
    HebrewObservationalDate

class HebrewSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(HebrewDate.from_fixed(self.testvalue), HebrewDate(5706, HebrewMonth.KISLEV, 7))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, HebrewDate(5706, HebrewMonth.KISLEV, 7).to_fixed())

class HebrewDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: HebrewDate(3174, 5, 10),
            -61387: HebrewDate(3593, 9, 25),
            25469: HebrewDate(3831, 7, 3),
            49217: HebrewDate(3896, 7, 9),
            171307: HebrewDate(4230, 10, 18),
            210155: HebrewDate(4336, 3, 4),
            253427: HebrewDate(4455, 8, 13),
            369740: HebrewDate(4773, 2, 6),
            400085: HebrewDate(4856, 2, 23),
            434355: HebrewDate(4950, 1, 7),
            452605: HebrewDate(5000, 13, 8),
            470160: HebrewDate(5048, 1, 21),
            473837: HebrewDate(5058, 2, 7),
            507850: HebrewDate(5151, 4, 1),
            524156: HebrewDate(5196, 11, 7),
            544676: HebrewDate(5252, 1, 3),
            567118: HebrewDate(5314, 7, 1),
            569477: HebrewDate(5320, 12, 27),
            601716: HebrewDate(5408, 3, 20),
            613424: HebrewDate(5440, 4, 3),
            626596: HebrewDate(5476, 5, 5),
            645554: HebrewDate(5528, 4, 4),
            664224: HebrewDate(5579, 5, 11),
            671401: HebrewDate(5599, 1, 12),
            694799: HebrewDate(5663, 1, 22),
            704424: HebrewDate(5689, 5, 19),
            708842: HebrewDate(5702, 7, 8),
            709409: HebrewDate(5703, 1, 14),
            709580: HebrewDate(5704, 7, 8),
            727274: HebrewDate(5752, 13, 12),
            728714: HebrewDate(5756, 12, 5),
            744313: HebrewDate(5799, 8, 12),
            764652: HebrewDate(5854, 5, 5)
        }
        
        for (fixed_date, hebrew_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, hebrew_date.to_fixed(), "Convert to fixed")
            self.assertEqual(HebrewDate.from_fixed(fixed_date), hebrew_date, "Convert from fixed")

class HebrewObservationalDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: HebrewObservationalDate(3174, 5, 11),
            -61387: HebrewObservationalDate(3593, 9, 24),
            25469: HebrewObservationalDate(3831, 7, 2),
            49217: HebrewObservationalDate(3896, 7, 7),
            171307: HebrewObservationalDate(4230, 10, 18),
            210155: HebrewObservationalDate(4336, 3, 3),
            253427: HebrewObservationalDate(4455, 9, 13),
            369740: HebrewObservationalDate(4773, 2, 5),
            400085: HebrewObservationalDate(4856, 2, 22),
            434355: HebrewObservationalDate(4950, 1, 7),
            452605: HebrewObservationalDate(5000, 13, 7),
            470160: HebrewObservationalDate(5048, 1, 21),
            473837: HebrewObservationalDate(5058, 2, 7),
            507850: HebrewObservationalDate(5151, 3, 30),
            524156: HebrewObservationalDate(5196, 12, 6),
            544676: HebrewObservationalDate(5252, 2, 2),
            567118: HebrewObservationalDate(5313, 6, 30),
            569477: HebrewObservationalDate(5320, 12, 27),
            601716: HebrewObservationalDate(5408, 3, 18),
            613424: HebrewObservationalDate(5440, 4, 3),
            626596: HebrewObservationalDate(5476, 5, 4),
            645554: HebrewObservationalDate(5528, 4, 4),
            664224: HebrewObservationalDate(5579, 5, 10),
            671401: HebrewObservationalDate(5599, 1, 11),
            694799: HebrewObservationalDate(5663, 1, 20),
            704424: HebrewObservationalDate(5689, 6, 19),
            708842: HebrewObservationalDate(5702, 7, 7),
            709409: HebrewObservationalDate(5703, 2, 14),
            709580: HebrewObservationalDate(5704, 8, 7),
            727274: HebrewObservationalDate(5752, 1, 12),
            728714: HebrewObservationalDate(5756, 12, 5),
            744313: HebrewObservationalDate(5799, 9, 12),
            764652: HebrewObservationalDate(5854, 5, 5)
        }
        
        for (fixed_date, hebrew_observational_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, hebrew_observational_date.to_fixed(), "Convert to fixed")
            self.assertEqual(HebrewObservationalDate.from_fixed(fixed_date), hebrew_observational_date, "Convert from fixed")

if __name__ == "__main__":
    unittest.main()