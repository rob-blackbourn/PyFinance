import unittest

from datetime import date

from py_finance.dates.calendars.united_kingdom import UnitedKingdom

class Test(unittest.TestCase):

    def setUp(self):
        self.calendar = UnitedKingdom()

    def tearDown(self):
        pass

    def testIsBusinessDay(self):
        self.assertFalse(self.calendar.is_business_day(date(2014, 12, 25)))


if __name__ == "__main__":
    unittest.main()