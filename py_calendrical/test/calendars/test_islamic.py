import unittest

from py_calendrical.calendars.islamic import ArithmeticIslamicDate,\
    ObservationalIslamicDate

class ArithmeticIslamicTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(ArithmeticIslamicDate.from_fixed(self.testvalue), ArithmeticIslamicDate(1364, 12, 6))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, ArithmeticIslamicDate(1364, 12, 6).to_fixed())

    def testKnownDates(self):
        knownDates = {
            -214193: ArithmeticIslamicDate(-1245, 12, 9),
            -61387: ArithmeticIslamicDate(-813, 2, 23),
            25469: ArithmeticIslamicDate(-568, 4, 1),
            49217: ArithmeticIslamicDate(-501, 4, 6),
            171307: ArithmeticIslamicDate(-157, 10, 17),
            210155: ArithmeticIslamicDate(-47, 6, 3),
            253427: ArithmeticIslamicDate(75, 7, 13),
            369740: ArithmeticIslamicDate(403, 10, 5),
            400085: ArithmeticIslamicDate(489, 5, 22),
            434355: ArithmeticIslamicDate(586, 2, 7),
            452605: ArithmeticIslamicDate(637, 8, 7),
            470160: ArithmeticIslamicDate(687, 2, 20),
            473837: ArithmeticIslamicDate(697, 7, 7),
            507850: ArithmeticIslamicDate(793, 7, 1),
            524156: ArithmeticIslamicDate(839, 7, 6),
            544676: ArithmeticIslamicDate(897, 6, 1),
            567118: ArithmeticIslamicDate(960, 9, 30),
            569477: ArithmeticIslamicDate(967, 5, 27),
            601716: ArithmeticIslamicDate(1058, 5, 18),
            613424: ArithmeticIslamicDate(1091, 6, 2),
            626596: ArithmeticIslamicDate(1128, 8, 4),
            645554: ArithmeticIslamicDate(1182, 2, 3),
            664224: ArithmeticIslamicDate(1234, 10, 10),
            671401: ArithmeticIslamicDate(1255, 1, 11),
            694799: ArithmeticIslamicDate(1321, 1, 21),
            704424: ArithmeticIslamicDate(1348, 3, 19),
            708842: ArithmeticIslamicDate(1360, 9, 8),
            709409: ArithmeticIslamicDate(1362, 4, 13),
            709580: ArithmeticIslamicDate(1362, 10, 7),
            727274: ArithmeticIslamicDate(1412, 9, 13),
            728714: ArithmeticIslamicDate(1416, 10, 5),
            744313: ArithmeticIslamicDate(1460, 10, 12),
            764652: ArithmeticIslamicDate(1518, 3, 5)
        }
        
        for (fixed_date, arithmetic_islamic_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, arithmetic_islamic_date.to_fixed(), "Convert to fixed")
            self.assertEqual(ArithmeticIslamicDate.from_fixed(fixed_date), arithmetic_islamic_date, "Convert from fixed")
        
class ObservationalIslamicTestCase(unittest.TestCase):
        
    def testKnownDates(self):
        knownDates = {
            -214193: ObservationalIslamicDate(-1245, 12, 11),
            -61387: ObservationalIslamicDate(-813, 2, 25),
            25469: ObservationalIslamicDate(-568, 4, 2),
            49217: ObservationalIslamicDate(-501, 4, 7),
            171307: ObservationalIslamicDate(-157, 10, 18),
            210155: ObservationalIslamicDate(-47, 6, 3),
            253427: ObservationalIslamicDate(75, 7, 13),
            369740: ObservationalIslamicDate(403, 10, 5),
            400085: ObservationalIslamicDate(489, 5, 22),
            434355: ObservationalIslamicDate(586, 2, 7),
            452605: ObservationalIslamicDate(637, 8, 7),
            470160: ObservationalIslamicDate(687, 2, 21),
            473837: ObservationalIslamicDate(697, 7, 7),
            507850: ObservationalIslamicDate(793, 6, 30),
            524156: ObservationalIslamicDate(839, 7, 6),
            544676: ObservationalIslamicDate(897, 6, 2),
            567118: ObservationalIslamicDate(960, 9, 30),
            569477: ObservationalIslamicDate(967, 5, 27),
            601716: ObservationalIslamicDate(1058, 5, 18),
            613424: ObservationalIslamicDate(1091, 6, 3),
            626596: ObservationalIslamicDate(1128, 8, 4),
            645554: ObservationalIslamicDate(1182, 2, 4),
            664224: ObservationalIslamicDate(1234, 10, 10),
            671401: ObservationalIslamicDate(1255, 1, 11),
            694799: ObservationalIslamicDate(1321, 1, 20),
            704424: ObservationalIslamicDate(1348, 3, 19),
            708842: ObservationalIslamicDate(1360, 9, 7),
            709409: ObservationalIslamicDate(1362, 4, 14),
            709580: ObservationalIslamicDate(1362, 10, 7),
            727274: ObservationalIslamicDate(1412, 9, 12),
            728714: ObservationalIslamicDate(1416, 10, 5),
            744313: ObservationalIslamicDate(1460, 10, 12),
            764652: ObservationalIslamicDate(1518, 3, 5)                      
        }

        for (fixed_date, observational_islamic_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, observational_islamic_date.to_fixed(), "Convert to fixed")
            self.assertEqual(ObservationalIslamicDate.from_fixed(fixed_date), observational_islamic_date, "Convert from fixed")
    
if __name__ == "__main__":
    unittest.main()