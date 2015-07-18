import unittest
from py_calendrical.day_arithmatic import DayOfWeek


class TestDayArithmatic(unittest.TestCase):

    def setUp(self):
        self.data = {
            -214193: DayOfWeek.Sunday,
            -61387 : DayOfWeek.Wednesday,
            25469  : DayOfWeek.Wednesday,
            49217  : DayOfWeek.Sunday,
            171307 : DayOfWeek.Wednesday,
            210155 : DayOfWeek.Monday,
            253427 : DayOfWeek.Saturday,
            369740 : DayOfWeek.Sunday,
            400085 : DayOfWeek.Sunday,
            434355 : DayOfWeek.Friday,
            452605 : DayOfWeek.Saturday,
            470160 : DayOfWeek.Friday,
            473837 : DayOfWeek.Sunday,
            507850 : DayOfWeek.Sunday,
            524156 : DayOfWeek.Wednesday,
            544676 : DayOfWeek.Saturday,
            567118 : DayOfWeek.Saturday,
            569477 : DayOfWeek.Saturday,
            601716 : DayOfWeek.Wednesday,
            613424 : DayOfWeek.Sunday,
            626596 : DayOfWeek.Friday,
            645554 : DayOfWeek.Sunday,
            664224 : DayOfWeek.Monday,
            671401 : DayOfWeek.Wednesday,
            694799 : DayOfWeek.Sunday,
            704424 : DayOfWeek.Sunday,
            708842 : DayOfWeek.Monday,
            709409 : DayOfWeek.Monday,
            709580 : DayOfWeek.Thursday,
            727274 : DayOfWeek.Tuesday,
            728714 : DayOfWeek.Sunday,
            744313 : DayOfWeek.Wednesday,
            764652 : DayOfWeek.Sunday }

    def testKnownData(self):
        for (fixed_date, day_of_week) in self.data.iteritems():
            self.assertEqual(day_of_week, DayOfWeek.from_fixed(fixed_date))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()