import unittest

from py_calendrical.calendars.ethiopic import EthiopicDate
from py_cal_cal.pycalcal import ethiopic_date

class EthiopicSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(EthiopicDate.from_fixed(self.testvalue), EthiopicDate(1938, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, EthiopicDate(1938, 3, 3).to_fixed())

    def testKnownDates(self):
        knownDates = {
            -214193: EthiopicDate(-594, 12, 6),
            -61387: EthiopicDate(-175, 4, 12),
            25469: EthiopicDate(63, 1, 29),
            49217: EthiopicDate(128, 2, 5),
            171307: EthiopicDate(462, 5, 12),
            210155: EthiopicDate(568, 9, 23),
            253427: EthiopicDate(687, 3, 11),
            369740: EthiopicDate(1005, 8, 24),
            400085: EthiopicDate(1088, 9, 23),
            434355: EthiopicDate(1182, 7, 20),
            452605: EthiopicDate(1232, 7, 7),
            470160: EthiopicDate(1280, 7, 30),
            473837: EthiopicDate(1290, 8, 25),
            507850: EthiopicDate(1383, 10, 10),
            524156: EthiopicDate(1428, 5, 29),
            544676: EthiopicDate(1484, 8, 5),
            567118: EthiopicDate(1546, 1, 12),
            569477: EthiopicDate(1552, 6, 29),
            601716: EthiopicDate(1640, 10, 6),
            613424: EthiopicDate(1672, 10, 26),
            626596: EthiopicDate(1708, 11, 19),
            645554: EthiopicDate(1760, 10, 14),
            664224: EthiopicDate(1811, 11, 27),
            671401: EthiopicDate(1831, 7, 19),
            694799: EthiopicDate(1895, 8, 11),
            704424: EthiopicDate(1921, 12, 19),
            708842: EthiopicDate(1934, 1, 19),
            709409: EthiopicDate(1935, 8, 11),
            709580: EthiopicDate(1936, 1, 26),
            727274: EthiopicDate(1984, 7, 8),
            728714: EthiopicDate(1988, 6, 17),
            744313: EthiopicDate(2031, 3, 1),
            764652: EthiopicDate(2086, 11, 11)                      
        }
        
        for (fixed_date, ethiopic_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, ethiopic_date.to_fixed(), "Convert to fixed")
            self.assertEqual(EthiopicDate.from_fixed(fixed_date), ethiopic_date, "Convert from fixed")
        
if __name__ == "__main__":
    unittest.main()