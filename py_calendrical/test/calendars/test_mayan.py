import unittest

from py_calendrical.calendars.mayan import MayanLongCountDate, MayanHaabDate, MayanTzolkinDate

class MayanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(MayanLongCountDate.from_fixed(self.testvalue), MayanLongCountDate(12, 16, 11, 16, 9))
        self.assertEqual(MayanLongCountDate.from_fixed(0), MayanLongCountDate(7, 17, 18, 13, 2))
        self.assertEqual(MayanHaabDate.from_fixed(self.testvalue), MayanHaabDate(11, 7))
        self.assertEqual(MayanTzolkinDate.from_fixed(self.testvalue), MayanTzolkinDate(11, 9))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, MayanLongCountDate(12, 16, 11, 16, 9).to_fixed())
        self.assertEqual(0, MayanLongCountDate(7, 17, 18, 13, 2).to_fixed())
        self.assertEqual(MayanHaabDate.on_or_before(MayanHaabDate(11, 7), self.testvalue), self.testvalue)
        self.assertEqual(MayanTzolkinDate.on_or_before(MayanTzolkinDate(11, 9), self.testvalue), self.testvalue)

class MayanLongCountDateTestCase(unittest.TestCase):
    
    def testKnwonDates(self):
        knownDates = {
            -214193: MayanLongCountDate(6, 8, 3, 13, 9),
            -61387: MayanLongCountDate(7, 9, 8, 3, 15),
            25469: MayanLongCountDate(8, 1, 9, 8, 11),
            49217: MayanLongCountDate(8, 4, 15, 7, 19),
            171307: MayanLongCountDate(9, 1, 14, 10, 9),
            210155: MayanLongCountDate(9, 7, 2, 8, 17),
            253427: MayanLongCountDate(9, 13, 2, 12, 9),
            369740: MayanLongCountDate(10, 9, 5, 14, 2),
            400085: MayanLongCountDate(10, 13, 10, 1, 7),
            434355: MayanLongCountDate(10, 18, 5, 4, 17),
            452605: MayanLongCountDate(11, 0, 15, 17, 7),
            470160: MayanLongCountDate(11, 3, 4, 13, 2),
            473837: MayanLongCountDate(11, 3, 14, 16, 19),
            507850: MayanLongCountDate(11, 8, 9, 7, 12),
            524156: MayanLongCountDate(11, 10, 14, 12, 18),
            544676: MayanLongCountDate(11, 13, 11, 12, 18),
            567118: MayanLongCountDate(11, 16, 14, 1, 0),
            569477: MayanLongCountDate(11, 17, 0, 10, 19),
            601716: MayanLongCountDate(12, 1, 10, 2, 18),
            613424: MayanLongCountDate(12, 3, 2, 12, 6),
            626596: MayanLongCountDate(12, 4, 19, 4, 18),
            645554: MayanLongCountDate(12, 7, 11, 16, 16),
            664224: MayanLongCountDate(12, 10, 3, 14, 6),
            671401: MayanLongCountDate(12, 11, 3, 13, 3),
            694799: MayanLongCountDate(12, 14, 8, 13, 1),
            704424: MayanLongCountDate(12, 15, 15, 8, 6),
            708842: MayanLongCountDate(12, 16, 7, 13, 4),
            709409: MayanLongCountDate(12, 16, 9, 5, 11),
            709580: MayanLongCountDate(12, 16, 9, 14, 2),
            727274: MayanLongCountDate(12, 18, 18, 16, 16),
            728714: MayanLongCountDate(12, 19, 2, 16, 16),
            744313: MayanLongCountDate(13, 1, 6, 4, 15),
            764652: MayanLongCountDate(13, 4, 2, 13, 14)
        }
        
        for (fixed_date, mayan_long_count_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, mayan_long_count_date.to_fixed(), "Convert to fixed")
            self.assertEqual(MayanLongCountDate.from_fixed(fixed_date), mayan_long_count_date, "Convert from fixed")

class MayanHaabDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: MayanHaabDate(11, 12),
            -61387: MayanHaabDate(5, 3),
            25469: MayanHaabDate(4, 9),
            49217: MayanHaabDate(5, 12),
            171307: MayanHaabDate(14, 12),
            210155: MayanHaabDate(4, 5),
            253427: MayanHaabDate(14, 7),
            369740: MayanHaabDate(8, 5),
            400085: MayanHaabDate(10, 15),
            434355: MayanHaabDate(8, 15),
            452605: MayanHaabDate(8, 15),
            470160: MayanHaabDate(10, 10),
            473837: MayanHaabDate(11, 17),
            507850: MayanHaabDate(15, 5),
            524156: MayanHaabDate(9, 6),
            544676: MayanHaabDate(13, 6),
            567118: MayanHaabDate(3, 18),
            569477: MayanHaabDate(12, 7),
            601716: MayanHaabDate(18, 6),
            613424: MayanHaabDate(1, 9),
            626596: MayanHaabDate(3, 1),
            645554: MayanHaabDate(1, 19),
            664224: MayanHaabDate(4, 14),
            671401: MayanHaabDate(16, 16),
            694799: MayanHaabDate(18, 14),
            704424: MayanHaabDate(7, 4),
            708842: MayanHaabDate(9, 2),
            709409: MayanHaabDate(19, 4),
            709580: MayanHaabDate(9, 10),
            727274: MayanHaabDate(18, 4),
            728714: MayanHaabDate(17, 4),
            744313: MayanHaabDate(12, 8),
            764652: MayanHaabDate(7, 7)
        }
        
        for (fixed_date, mayan_haab_date) in knownDates.iteritems():
            self.assertEqual(MayanHaabDate.from_fixed(fixed_date), mayan_haab_date, "Convert from fixed")

class MayanTzolkinDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: MayanTzolkinDate(5, 9),
            -61387: MayanTzolkinDate(9, 15),
            25469: MayanTzolkinDate(12, 11),
            49217: MayanTzolkinDate(9, 19),
            171307: MayanTzolkinDate(3, 9),
            210155: MayanTzolkinDate(7, 17),
            253427: MayanTzolkinDate(2, 9),
            369740: MayanTzolkinDate(4, 2),
            400085: MayanTzolkinDate(7, 7),
            434355: MayanTzolkinDate(9, 17),
            452605: MayanTzolkinDate(7, 7),
            470160: MayanTzolkinDate(12, 2),
            473837: MayanTzolkinDate(10, 19),
            507850: MayanTzolkinDate(2, 12),
            524156: MayanTzolkinDate(6, 18),
            544676: MayanTzolkinDate(12, 18),
            567118: MayanTzolkinDate(3, 20),
            569477: MayanTzolkinDate(9, 19),
            601716: MayanTzolkinDate(8, 18),
            613424: MayanTzolkinDate(3, 6),
            626596: MayanTzolkinDate(6, 18),
            645554: MayanTzolkinDate(10, 16),
            664224: MayanTzolkinDate(12, 6),
            671401: MayanTzolkinDate(13, 3),
            694799: MayanTzolkinDate(11, 1),
            704424: MayanTzolkinDate(3, 6),
            708842: MayanTzolkinDate(1, 4),
            709409: MayanTzolkinDate(9, 11),
            709580: MayanTzolkinDate(11, 2),
            727274: MayanTzolkinDate(12, 16),
            728714: MayanTzolkinDate(9, 16),
            744313: MayanTzolkinDate(8, 15),
            764652: MayanTzolkinDate(2, 14)
        }
        
        for (fixed_date, mayan_tzolkin_date) in knownDates.iteritems():
            self.assertEqual(MayanTzolkinDate.from_fixed(fixed_date), mayan_tzolkin_date, "Convert from fixed")

if __name__ == "__main__":
    unittest.main()