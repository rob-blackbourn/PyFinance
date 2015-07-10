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
        
    def test_is_end_of_month(self):
        self.assertFalse(Calendar.is_end_of_month(date(2008, 1, 30)), "30 January is not the end of the month")
        self.assertTrue(Calendar.is_end_of_month(date(2008, 1, 31)), "31 January is the end of the month")
        self.assertFalse(Calendar.is_end_of_month(date(2008, 2, 28)), "28 February 2008 is not the end of the month because it's a leap year")
        self.assertTrue(Calendar.is_end_of_month(date(2008, 2, 29)), "28 February 2008 is the end of the month because it's a leap year")
        self.assertTrue(Calendar.is_end_of_month(date(2009, 2, 28)), "28 February 2009 is the end of the month because it's a not leap year")
    
    def test_constructor(self):
        c1 = Calendar("empty")
        self.assertTrue(isinstance(c1.holidays, list), "Should have a holiday list")
        self.assertEqual(0, len(c1.holidays), "Should have an empty holiday list")
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(isinstance(c2.holidays, list), "Should have an empty holiday list")
        self.assertEqual(2, len(c2.holidays), "Should have an empty holiday list")
        
    def test_is_holiday(self):
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(c2.is_holiday(date(2014, 12, 25)), "Thursday 25 December 2014 is a holiday")
        self.assertTrue(c2.is_holiday(date(2014, 12, 26)), "Friday 26 December 2014 is a holiday")
        self.assertFalse(c2.is_holiday(date(2014, 12, 27)), "Saturday 27 December 2014 is not a holiday")
    
    def test_is_business_day(self):
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(c2.is_business_day(date(2014, 12, 24)), "Wednesday 24 December 2014 is a business day")
        self.assertFalse(c2.is_business_day(date(2014, 12, 25)), "Thursday 25 December 2014 is not a business day")
        self.assertFalse(c2.is_business_day(date(2014, 12, 26)), "Friday 26 December 2014 is not a business day")
        self.assertFalse(c2.is_business_day(date(2014, 12, 27)), "Saturday 27 December 2014 is not a business day")
        self.assertFalse(c2.is_business_day(date(2014, 12, 28)), "Sunday 28 December 2014 is not a business day")
        self.assertTrue(c2.is_business_day(date(2014, 12, 29)), "Monday 29 December 2014 is a business day")
        
if __name__ == "__main__":
    unittest.main()