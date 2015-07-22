import unittest

from py_calendrical.calendars.bahai import WesternBahaiDate, FutureBahaiDate

class WesternBahaiDateTestCase(unittest.TestCase):

    def testKnownDates(self):
        knownDates = {
            -214193: WesternBahaiDate(-6, 6, 3, 7, 12),
            -61387: WesternBahaiDate(-5, 9, 3, 14, 13),
            25469: WesternBahaiDate(-4, 2, 13, 10, 17),
            49217: WesternBahaiDate(-4, 6, 2, 11, 6),
            171307: WesternBahaiDate(-3, 4, 13, 16, 9),
            210155: WesternBahaiDate(-3, 10, 6, 4, 4),
            253427: WesternBahaiDate(-3, 16, 10, 13, 7),
            369740: WesternBahaiDate(-2, 14, 6, 2, 17),
            400085: WesternBahaiDate(-2, 18, 13, 4, 8),
            434355: WesternBahaiDate(-1, 4, 12, 1, 3),
            452605: WesternBahaiDate(-1, 7, 4, 19, 9),
            470160: WesternBahaiDate(-1, 9, 15, 1, 13),
            473837: WesternBahaiDate(-1, 10, 6, 2, 19),
            507850: WesternBahaiDate(-1, 15, 4, 5, 8),
            524156: WesternBahaiDate(-1, 17, 10, 17, 16),
            544676: WesternBahaiDate(0, 1, 10, 2, 1),
            567118: WesternBahaiDate(0, 4, 14, 10, 12),
            569477: WesternBahaiDate(0, 5, 1, 19, 4),
            601716: WesternBahaiDate(0, 9, 14, 5, 6),
            613424: WesternBahaiDate(0, 11, 8, 6, 7),
            626596: WesternBahaiDate(0, 13, 6, 7, 12),
            645554: WesternBahaiDate(0, 16, 1, 5, 15),
            664224: WesternBahaiDate(0, 18, 14, 8, 2),
            671401: WesternBahaiDate(0, 19, 15, 1, 7),
            694799: WesternBahaiDate(1, 4, 3, 2, 11),
            704424: WesternBahaiDate(1, 5, 10, 9, 6),
            708842: WesternBahaiDate(1, 6, 3, 11, 3),
            709409: WesternBahaiDate(1, 6, 5, 2, 11),
            709580: WesternBahaiDate(1, 6, 5, 11, 11),
            727274: WesternBahaiDate(1, 8, 15, 19, 16),
            728714: WesternBahaiDate(1, 8, 19, 18, 19),
            744313: WesternBahaiDate(1, 11, 5, 13, 7),
            764652: WesternBahaiDate(1, 14, 4, 7, 6)
        }

        for (fixed_date, western_bahai_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, western_bahai_date.to_fixed(), "Convert to fixed")
            self.assertEqual(WesternBahaiDate.from_fixed(fixed_date), western_bahai_date, "Convert from fixed")

class FutureBahaiDateTestCase(unittest.TestCase):
    
    def testKnownDates(self):
        knownDates = {
            -214193: FutureBahaiDate(-6, 6, 3, 7, 11),
            -61387: FutureBahaiDate(-5, 9, 3, 14, 13),
            25469: FutureBahaiDate(-4, 2, 13, 10, 18),
            49217: FutureBahaiDate(-4, 6, 2, 11, 6),
            171307: FutureBahaiDate(-3, 4, 13, 16, 10),
            210155: FutureBahaiDate(-3, 10, 6, 4, 5),
            253427: FutureBahaiDate(-3, 16, 10, 13, 7),
            369740: FutureBahaiDate(-2, 14, 6, 2, 17),
            400085: FutureBahaiDate(-2, 18, 13, 4, 9),
            434355: FutureBahaiDate(-1, 4, 12, 1, 3),
            452605: FutureBahaiDate(-1, 7, 4, 19, 10),
            470160: FutureBahaiDate(-1, 9, 15, 1, 14),
            473837: FutureBahaiDate(-1, 10, 6, 3, 1),
            507850: FutureBahaiDate(-1, 15, 4, 5, 8),
            524156: FutureBahaiDate(-1, 17, 10, 17, 16),
            544676: FutureBahaiDate(0, 1, 10, 2, 2),
            567118: FutureBahaiDate(0, 4, 14, 10, 12),
            569477: FutureBahaiDate(0, 5, 1, 19, 4),
            601716: FutureBahaiDate(0, 9, 14, 5, 7),
            613424: FutureBahaiDate(0, 11, 8, 6, 8),
            626596: FutureBahaiDate(0, 13, 6, 7, 13),
            645554: FutureBahaiDate(0, 16, 1, 5, 16),
            664224: FutureBahaiDate(0, 18, 14, 8, 2),
            671401: FutureBahaiDate(0, 19, 15, 1, 7),
            694799: FutureBahaiDate(1, 4, 3, 2, 10),
            704424: FutureBahaiDate(1, 5, 10, 9, 6),
            708842: FutureBahaiDate(1, 6, 3, 11, 3),
            709409: FutureBahaiDate(1, 6, 5, 2, 11),
            709580: FutureBahaiDate(1, 6, 5, 11, 11),
            727274: FutureBahaiDate(1, 8, 15, 19, 17),
            728714: FutureBahaiDate(1, 8, 19, 18, 19),
            744313: FutureBahaiDate(1, 11, 5, 13, 8),
            764652: FutureBahaiDate(1, 14, 4, 7, 7)
        }

        for (fixed_date, future_bahai_date) in knownDates.iteritems():
            self.assertEqual(fixed_date, future_bahai_date.to_fixed(), "Convert to fixed")
            self.assertEqual(FutureBahaiDate.from_fixed(fixed_date), future_bahai_date, "Convert from fixed")

if __name__ == "__main__":
    unittest.main()