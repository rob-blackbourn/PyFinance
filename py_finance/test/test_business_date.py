import unittest
from py_finance.business_date import business_date
from datetime import datetime

class Test_business_date(unittest.TestCase):

    def testConstructor(self):
        d = business_date(1967, 8, 12)
        self.assertEqual(1967, d.year, "invalid year")
        self.assertEqual(8, d.month, "invalid month")
        self.assertEqual(12, d.day, "invalid day")

    def test_is_weekday(self):
        # Monday 1 December, 2014
        d1 = business_date(2014, 12, 1)
        self.assertTrue(d1.is_weekday(), "Should detect Monday as a weekday")
        # Saturday 6 December, 2014
        d2 = business_date(2014, 12, 6)
        self.assertFalse(d2.is_weekday(), "Should detect Saturday as a weekend")

    def test_is_weekend(self):
        # Monday 1 December, 2014
        d1 = business_date(2014, 12, 1)
        self.assertFalse(d1.is_weekend(), "Should detect Monday as a weekday")
        # Saturday 6 December, 2014
        d2 = business_date(2014, 12, 6)
        self.assertTrue(d2.is_weekend(), "Should detect Saturday as a weekend")

    def test_is_holiday(self):
        # Thursday 25 December, 2014
        holidays = (datetime(2014, 12, 25),)
        d1 = business_date(2014, 12, 25, holidays)
        self.assertTrue(d1.is_holiday(), "Christmas day is a holiday")
        d2 = business_date(2014, 12, 24, holidays)
        self.assertFalse(d2.is_holiday(), "Christmas eve is not a holiday")
        
        
if __name__ == "__main__":
    unittest.main()