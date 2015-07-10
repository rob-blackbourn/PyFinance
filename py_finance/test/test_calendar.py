import unittest
from datetime import date
from py_finance.calendar import Calendar, business_day_convention

class TestCalendar(unittest.TestCase):

    def test_is_leap_year(self):
        self.assertTrue(Calendar.is_leap_year(2008), "Is a leap year.")
        self.assertFalse(Calendar.is_leap_year(2009), "Isn't a leap year.")
        self.assertFalse(Calendar.is_leap_year(2010), "Isn't a leap year.")
        self.assertFalse(Calendar.is_leap_year(2011), "Isn't a leap year.")
        self.assertTrue(Calendar.is_leap_year(2012), "Is a leap year.")
        self.assertFalse(Calendar.is_leap_year(2013), "Isn't a leap year.")
        self.assertFalse(Calendar.is_leap_year(2014), "Isn't a leap year.")
        self.assertFalse(Calendar.is_leap_year(2015), "Isn't a leap year.")
        self.assertTrue(Calendar.is_leap_year(2016), "Is a leap year.")
        self.assertFalse(Calendar.is_leap_year(2100), "Isn't a leap year.")

    def test_days_in_month(self):
        self.assertEqual(31, Calendar.days_in_month(2009, 1), "There are 28 days in January.")
        self.assertEqual(28, Calendar.days_in_month(2009, 2), "There are 28 days in February in a non leap year.")
        self.assertEqual(31, Calendar.days_in_month(2009, 3), "There are 28 days in March.")
        self.assertEqual(30, Calendar.days_in_month(2009, 4), "There are 28 days in April.")
        self.assertEqual(31, Calendar.days_in_month(2009, 5), "There are 28 days in May.")
        self.assertEqual(30, Calendar.days_in_month(2009, 6), "There are 28 days in June.")
        self.assertEqual(31, Calendar.days_in_month(2009, 7), "There are 28 days in July.")
        self.assertEqual(31, Calendar.days_in_month(2009, 8), "There are 28 days in August.")
        self.assertEqual(30, Calendar.days_in_month(2009, 9), "There are 30 days in September.")
        self.assertEqual(31, Calendar.days_in_month(2009, 10), "There are 28 days in October.")
        self.assertEqual(30, Calendar.days_in_month(2009, 11), "There are 28 days in November.")
        self.assertEqual(31, Calendar.days_in_month(2009, 12), "There are 28 days in December.")
        self.assertEqual(29, Calendar.days_in_month(2008, 2), "There are 29 days in February in a leap year.")

    def test_is_weekend(self):
        self.assertFalse(Calendar.is_weekend(date(2014, 12, 19)), "19 December 2014 was a Friday.")
        self.assertTrue(Calendar.is_weekend(date(2014, 12, 20)), "20 December 2014 was a Saturday.")
        self.assertTrue(Calendar.is_weekend(date(2014, 12, 21)), "21 December 2014 was a Sunday.")
        self.assertFalse(Calendar.is_weekend(date(2014, 12, 22)), "22 December 2014 was a Monday.")
        
    def test_is_end_of_month(self):
        self.assertFalse(Calendar.is_end_of_month(date(2008, 1, 30)), "30 January is not the end of the month.")
        self.assertTrue(Calendar.is_end_of_month(date(2008, 1, 31)), "31 January is the end of the month.")
        self.assertFalse(Calendar.is_end_of_month(date(2008, 2, 28)), "28 February 2008 is not the end of the month because it's a leap year.")
        self.assertTrue(Calendar.is_end_of_month(date(2008, 2, 29)), "28 February 2008 is the end of the month because it's a leap year.")
        self.assertTrue(Calendar.is_end_of_month(date(2009, 2, 28)), "28 February 2009 is the end of the month because it's a not leap year.")
    
    def test_constructor(self):
        c1 = Calendar("empty")
        self.assertTrue(isinstance(c1.holidays, list), "Should have a holiday list.")
        self.assertEqual(0, len(c1.holidays), "Should have an empty holiday list.")
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(isinstance(c2.holidays, list), "Should have an empty holiday list.")
        self.assertEqual(2, len(c2.holidays), "Should have an empty holiday list.")
        
    def test_is_holiday(self):
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(c2.is_holiday(date(2014, 12, 25)), "Thursday 25 December 2014 is a holiday.")
        self.assertTrue(c2.is_holiday(date(2014, 12, 26)), "Friday 26 December 2014 is a holiday.")
        self.assertFalse(c2.is_holiday(date(2014, 12, 27)), "Saturday 27 December 2014 is not a holiday.")
    
    def test_is_business_day(self):
        c2 = Calendar("Christmas", (date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(c2.is_business_day(date(2014, 12, 24)), "Wednesday 24 December 2014 is a business day.")
        self.assertFalse(c2.is_business_day(date(2014, 12, 25)), "Thursday 25 December 2014 is not a business day.")
        self.assertFalse(c2.is_business_day(date(2014, 12, 26)), "Friday 26 December 2014 is not a business day.")
        self.assertFalse(c2.is_business_day(date(2014, 12, 27)), "Saturday 27 December 2014 is not a business day.")
        self.assertFalse(c2.is_business_day(date(2014, 12, 28)), "Sunday 28 December 2014 is not a business day.")
        self.assertTrue(c2.is_business_day(date(2014, 12, 29)), "Monday 29 December 2014 is a business day.")
    
    def test_add_months(self):
        # Forward
        self.assertEqual(date(2013, 2, 28), Calendar.add_months(date(2012, 11, 30), 3), "Should not roll into March.")
        self.assertEqual(date(2013, 4, 28), Calendar.add_months(date(2013, 2, 28), 2, False), "Should not go to end of month.")
        self.assertEqual(date(2013, 4, 30), Calendar.add_months(date(2013, 2, 28), 2, True), "Should go to end of month.")
        self.assertEqual(date(2013, 1, 30), Calendar.add_months(date(2012, 11, 30), 2, False), "Should not go to end of month.")
        self.assertEqual(date(2013, 1, 31), Calendar.add_months(date(2012, 11, 30), 2, True), "Should go to end of month.")
        # Back
        self.assertEqual(date(2012, 11, 28), Calendar.add_months(date(2013, 2, 28), -3, False), "Should not roll into March.")
        self.assertEqual(date(2012, 11, 30), Calendar.add_months(date(2013, 2, 28), -3, True), "Should go to end of month.")
        self.assertEqual(date(2013, 1, 28), Calendar.add_months(date(2013, 4, 28), -3, True), "Should not go to end of month.")
        self.assertEqual(date(2012, 1, 28), Calendar.add_months(date(2013, 4, 28), -15, True), "Should not go to end of month.")
        self.assertEqual(date(2013, 4, 30), Calendar.add_months(date(2013, 5, 31), -1, True), "Should not stay in May.")
        self.assertEqual(date(2013, 4, 30), Calendar.add_months(date(2013, 5, 31), -1, False), "Should not stay in May.")
    
    def test_add_business_days(self):
        cal = Calendar("TARGET", (date(2015, 1, 1), date(2015, 4, 3), date(2015, 4, 6), date(2015, 5, 1), date(2015, 12, 25), date(2015, 12, 16)))
        # Forward
        self.assertEqual(date(2015, 1, 8), cal.add_business_days(date(2015, 1, 1), 5), "Should skip New Years Day.")
        self.assertEqual(date(2015, 1, 8), cal.add_business_days(date(2015, 1, 2), 4), "Nothing to skip.")
        self.assertEqual(date(2015, 1, 2), cal.add_business_days(date(2014, 12, 29), 3), "Nothing to skip.")
        # Back
        self.assertEqual(date(2014, 12, 31), cal.add_business_days(date(2015, 1, 8), -5), "Should skip New Years Day.")
        self.assertEqual(date(2015, 1, 2), cal.add_business_days(date(2015, 1, 8), -4), "Nothing to skip.")
        self.assertEqual(date(2014, 12, 29), cal.add_business_days(date(2015, 1, 2), -3), "Nothing to skip.")
    
    def test_adjust(self):
        cal = Calendar("TARGET", (date(2015, 1, 1), date(2015, 4, 3), date(2015, 4, 6), date(2015, 5, 1), date(2015, 12, 25), date(2015, 12, 16)))

        jan_first = date(2015, 1, 1)
        jan_second = date(2015, 1, 2)
        
        # business_day_convention.none
        self.assertEqual(jan_first, cal.adjust(jan_first, business_day_convention.none), "No adjustment.")
        
        # business_day_convention.following
        self.assertEqual(jan_second, cal.adjust(jan_first, business_day_convention.following), "Adjusted to January 2.")
    
if __name__ == "__main__":
    unittest.main()