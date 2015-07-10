import unittest
from datetime import date
from py_finance.calendar import Calendar

class TestCalendar(unittest.TestCase):

    def test_is_leap_year(self):
        self.assertTrue(Calendar.is_leap_year(2008))
        self.assertFalse(Calendar.is_leap_year(2009))
        self.assertFalse(Calendar.is_leap_year(2010))
        self.assertFalse(Calendar.is_leap_year(2011))
        self.assertTrue(Calendar.is_leap_year(2012))
        self.assertFalse(Calendar.is_leap_year(2013))
        self.assertFalse(Calendar.is_leap_year(2014))
        self.assertFalse(Calendar.is_leap_year(2015))
        self.assertTrue(Calendar.is_leap_year(2016))
        self.assertFalse(Calendar.is_leap_year(2100))

    def test_days_in_month(self):
        self.assertEqual(31, Calendar.days_in_month(2009, 1), "There are 28 days in January")
        self.assertEqual(28, Calendar.days_in_month(2009, 2), "There are 28 days in February in a non leap year")
        self.assertEqual(31, Calendar.days_in_month(2009, 3), "There are 28 days in March")
        self.assertEqual(30, Calendar.days_in_month(2009, 4), "There are 28 days in April")
        self.assertEqual(31, Calendar.days_in_month(2009, 5), "There are 28 days in May")
        self.assertEqual(30, Calendar.days_in_month(2009, 6), "There are 28 days in June")
        self.assertEqual(31, Calendar.days_in_month(2009, 7), "There are 28 days in July")
        self.assertEqual(31, Calendar.days_in_month(2009, 8), "There are 28 days in August")
        self.assertEqual(30, Calendar.days_in_month(2009, 9), "There are 30 days in September")
        self.assertEqual(31, Calendar.days_in_month(2009, 10), "There are 28 days in October")
        self.assertEqual(30, Calendar.days_in_month(2009, 11), "There are 28 days in November")
        self.assertEqual(31, Calendar.days_in_month(2009, 12), "There are 28 days in December")
        self.assertEqual(29, Calendar.days_in_month(2008, 2), "There are 29 days in February in a leap year")

    def test_is_weekend(self):
        self.assertFalse(Calendar.is_weekend(date(2014, 12, 19)), "19 December 2014 was a Friday")
        self.assertTrue(Calendar.is_weekend(date(2014, 12, 20)), "20 December 2014 was a Saturday")
        self.assertTrue(Calendar.is_weekend(date(2014, 12, 21)), "21 December 2014 was a Sunday")
        self.assertFalse(Calendar.is_weekend(date(2014, 12, 22)), "22 December 2014 was a Monday")
        
        
if __name__ == "__main__":
    unittest.main()