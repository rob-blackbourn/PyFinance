import unittest
from py_calendrical.calendars.aztec import AztecXihuitlDate,\
    AztecTonalpohualliDate


class AztecSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(AztecXihuitlDate.from_fixed(self.testvalue), AztecXihuitlDate(2, 1))

    def testConversionToFixed(self):
        self.assertEqual(AztecXihuitlDate.on_or_before(AztecXihuitlDate(2, 1), self.testvalue), self.testvalue)

class AztecXihuitlDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: AztecXihuitlDate(2, 6),
            -61387: AztecXihuitlDate(14, 2),
            25469: AztecXihuitlDate(13, 8),
            49217: AztecXihuitlDate(14, 11),
            171307: AztecXihuitlDate(5, 6),
            210155: AztecXihuitlDate(13, 4),
            253427: AztecXihuitlDate(5, 1),
            369740: AztecXihuitlDate(17, 4),
            400085: AztecXihuitlDate(1, 9),
            434355: AztecXihuitlDate(17, 14),
            452605: AztecXihuitlDate(17, 14),
            470160: AztecXihuitlDate(1, 4),
            473837: AztecXihuitlDate(2, 11),
            507850: AztecXihuitlDate(5, 19),
            524156: AztecXihuitlDate(18, 5),
            544676: AztecXihuitlDate(3, 20),
            567118: AztecXihuitlDate(12, 17),
            569477: AztecXihuitlDate(3, 1),
            601716: AztecXihuitlDate(8, 20),
            613424: AztecXihuitlDate(10, 8),
            626596: AztecXihuitlDate(11, 20),
            645554: AztecXihuitlDate(10, 18),
            664224: AztecXihuitlDate(13, 13),
            671401: AztecXihuitlDate(7, 10),
            694799: AztecXihuitlDate(9, 8),
            704424: AztecXihuitlDate(16, 3),
            708842: AztecXihuitlDate(18, 1),
            709409: AztecXihuitlDate(9, 18),
            709580: AztecXihuitlDate(18, 9),
            727274: AztecXihuitlDate(8, 18),
            728714: AztecXihuitlDate(7, 18),
            744313: AztecXihuitlDate(3, 2),
            764652: AztecXihuitlDate(16, 6)
        }
        
        for (fixed_date, aztec_xihuitl_date) in knownDates.iteritems():
            self.assertEqual(AztecXihuitlDate.from_fixed(fixed_date), aztec_xihuitl_date, "Convert from fixed")
        
class AztecTonalpohualliDateTestCase(unittest.TestCase):        
    
    def testKnwonDates(self):
        knownDates = {
            -214193: AztecTonalpohualliDate(5, 9),
            -61387: AztecTonalpohualliDate(9, 15),
            25469: AztecTonalpohualliDate(12, 11),
            49217: AztecTonalpohualliDate(9, 19),
            171307: AztecTonalpohualliDate(3, 9),
            210155: AztecTonalpohualliDate(7, 17),
            253427: AztecTonalpohualliDate(2, 9),
            369740: AztecTonalpohualliDate(4, 2),
            400085: AztecTonalpohualliDate(7, 7),
            434355: AztecTonalpohualliDate(9, 17),
            452605: AztecTonalpohualliDate(7, 7),
            470160: AztecTonalpohualliDate(12, 2),
            473837: AztecTonalpohualliDate(10, 19),
            507850: AztecTonalpohualliDate(2, 12),
            524156: AztecTonalpohualliDate(6, 18),
            544676: AztecTonalpohualliDate(12, 18),
            567118: AztecTonalpohualliDate(3, 20),
            569477: AztecTonalpohualliDate(9, 19),
            601716: AztecTonalpohualliDate(8, 18),
            613424: AztecTonalpohualliDate(3, 6),
            626596: AztecTonalpohualliDate(6, 18),
            645554: AztecTonalpohualliDate(10, 16),
            664224: AztecTonalpohualliDate(12, 6),
            671401: AztecTonalpohualliDate(13, 3),
            694799: AztecTonalpohualliDate(11, 1),
            704424: AztecTonalpohualliDate(3, 6),
            708842: AztecTonalpohualliDate(1, 4),
            709409: AztecTonalpohualliDate(9, 11),
            709580: AztecTonalpohualliDate(11, 2),
            727274: AztecTonalpohualliDate(12, 16),
            728714: AztecTonalpohualliDate(9, 16),
            744313: AztecTonalpohualliDate(8, 15),
            764652: AztecTonalpohualliDate(2, 14)
        }
        
        for (fixed_date, aztec_tonalpohualli_date) in knownDates.iteritems():
            self.assertEqual(AztecTonalpohualliDate.from_fixed(fixed_date), aztec_tonalpohualli_date, "Convert from fixed")
        
if __name__ == "__main__":
    unittest.main()