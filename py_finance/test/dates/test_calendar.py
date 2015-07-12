import unittest
from datetime import date
from py_finance.dates.calendar import Calendar
from py_finance.dates.simple_calendar import SimpleCalendar
from py_finance.dates.business_day_convention import BusinessDayConvention
from py_finance.dates.calendar_month import CalendarMonth
from py_finance.dates.day_of_week import DayOfWeek

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
        
    def test_is_holiday(self):
        c2 = SimpleCalendar((date(2014, 12, 25), date(2014, 12, 26)))
        self.assertTrue(c2.is_holiday(date(2014, 12, 25)), "Thursday 25 December 2014 is a holiday.")
        self.assertTrue(c2.is_holiday(date(2014, 12, 26)), "Friday 26 December 2014 is a holiday.")
        self.assertFalse(c2.is_holiday(date(2014, 12, 27)), "Saturday 27 December 2014 is not a holiday.")
    
    def test_is_business_day(self):
        c2 = SimpleCalendar((date(2014, 12, 25), date(2014, 12, 26)))
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
    
    def test_easter(self):
        self.assertEquals(date(2001, 4, 15), Calendar.easter(2001), "Easter 2001")
        self.assertEquals(date(2002, 3, 31), Calendar.easter(2002), "Easter 2002")
        self.assertEquals(date(2003, 4, 20), Calendar.easter(2003), "Easter 2003")
        self.assertEquals(date(2004, 4, 11), Calendar.easter(2004), "Easter 2004")
        self.assertEquals(date(2005, 3, 27), Calendar.easter(2005), "Easter 2005")
        self.assertEquals(date(2006, 4, 16), Calendar.easter(2006), "Easter 2006")
        self.assertEquals(date(2007, 4, 8), Calendar.easter(2007), "Easter 2007")
        self.assertEquals(date(2008, 3, 23), Calendar.easter(2008), "Easter 2008")
        self.assertEquals(date(2009, 4, 12), Calendar.easter(2009), "Easter 2009")
        self.assertEquals(date(2010, 4, 4), Calendar.easter(2010), "Easter 2010")
        self.assertEquals(date(2011, 4, 24), Calendar.easter(2011), "Easter 2011")
        self.assertEquals(date(2012, 4, 8), Calendar.easter(2012), "Easter 2012")
        self.assertEquals(date(2013, 3, 31), Calendar.easter(2013), "Easter 2013")
        self.assertEquals(date(2014, 4, 20), Calendar.easter(2014), "Easter 2014")
        self.assertEquals(date(2015, 4, 5), Calendar.easter(2015), "Easter 2015")
        self.assertEquals(date(2016, 3, 27), Calendar.easter(2016), "Easter 2016")
        self.assertEquals(date(2017, 4, 16), Calendar.easter(2017), "Easter 2017")
        self.assertEquals(date(2018, 4, 1), Calendar.easter(2018), "Easter 2018")
        self.assertEquals(date(2019, 4, 21), Calendar.easter(2019), "Easter 2019")
        self.assertEquals(date(2020, 4, 12), Calendar.easter(2020), "Easter 2020")
        self.assertEquals(date(2021, 4, 4), Calendar.easter(2021), "Easter 2021")

    def test_add_business_days(self):
        cal = SimpleCalendar((date(2015, 1, 1), date(2015, 4, 3), date(2015, 4, 6), date(2015, 5, 1), date(2015, 12, 25), date(2015, 12, 16)))
        # Forward
        self.assertEqual(date(2015, 1, 8), cal.add_business_days(date(2015, 1, 1), 5), "Should skip New Years Day.")
        self.assertEqual(date(2015, 1, 8), cal.add_business_days(date(2015, 1, 2), 4), "Nothing to skip.")
        self.assertEqual(date(2015, 1, 2), cal.add_business_days(date(2014, 12, 29), 3), "Nothing to skip.")
        # Back
        self.assertEqual(date(2014, 12, 31), cal.add_business_days(date(2015, 1, 8), -5), "Should skip New Years Day.")
        self.assertEqual(date(2015, 1, 2), cal.add_business_days(date(2015, 1, 8), -4), "Nothing to skip.")
        self.assertEqual(date(2014, 12, 29), cal.add_business_days(date(2015, 1, 2), -3), "Nothing to skip.")
    
    def test_nearest_business_day(self):
        #              July 2015
        # Su Mo Tu We Th Fr Sa
        #           1  2  3  4
        #  5  6  7  8  9 10 11
        # 12 13 14 15 16 17 18
        # 19 20 21 22 23 24 25
        # 26 27 28 29 30 31
        cal = SimpleCalendar([date(2015, 7, 13)])
        self.assertEquals(date(2015, 7, 3), cal.nearest_business_day(date(2015, 7, 4)), "Saturday should roll to Friday")
        self.assertEquals(date(2015, 7, 6), cal.nearest_business_day(date(2015, 7, 5)), "Sunday should roll to Monday")
        self.assertEquals(date(2015, 7, 14), cal.nearest_business_day(date(2015, 7, 12), True), "Sunday should prefer to roll to Tuesday")
        self.assertEquals(date(2015, 7, 10), cal.nearest_business_day(date(2015, 7, 12), False), "Sunday should prefer to roll to Friday")
        
    def test_add_nth_day_of_week(self):
        #      June 2015
        # Su Mo Tu We Th Fr Sa
        #     1  2  3  4  5  6
        #  7  8  9 10 11 12 13
        # 14 15 16 17 18 19 20
        # 21 22 23 24 25 26 27
        # 28 29 30
        self.assertEqual(date(2015, 6, 1), Calendar.add_nth_day_of_week(date(2015, 6, 1), 1, DayOfWeek.monday, False), "The first Monday is the same date.")
        self.assertEqual(date(2015, 6, 8), Calendar.add_nth_day_of_week(date(2015, 6, 1), 1, DayOfWeek.monday, True), "When strictly different go to the next week.")
        self.assertEqual(date(2015, 6, 2), Calendar.add_nth_day_of_week(date(2015, 6, 1), 1, DayOfWeek.tuesday, False), "The first Tuesday is the next date.")
        self.assertEqual(date(2015, 6, 2), Calendar.add_nth_day_of_week(date(2015, 6, 1), 1, DayOfWeek.tuesday, True), "Strictly different should make no difference.")
        self.assertEqual(date(2015, 6, 17), Calendar.add_nth_day_of_week(date(2015, 6, 1), 3, DayOfWeek.wednesday, False), "Third Wednesday.")
        self.assertEqual(date(2015, 6, 30), Calendar.add_nth_day_of_week(date(2015, 6, 30), -1, DayOfWeek.tuesday, False), "The last Tuesday is the same date.")
        self.assertEqual(date(2015, 6, 23), Calendar.add_nth_day_of_week(date(2015, 6, 30), -1, DayOfWeek.tuesday, True), "Skip the start date as it's a Tuesday.")
        self.assertEqual(date(2015, 6, 10), Calendar.add_nth_day_of_week(date(2015, 6, 30), -3, DayOfWeek.wednesday, True), "Third Wednesday from the end of the month..")
    
    def test_adjust(self):
        cal = SimpleCalendar((date(2015, 1, 1), date(2015, 4, 3), date(2015, 4, 6), date(2015, 5, 1), date(2015, 12, 25), date(2015, 12, 16)))

        jan_first = date(2015, 1, 1)
        jan_second = date(2015, 1, 2)
        
        # BusinessDayConvention.none
        self.assertEqual(jan_first, cal.adjust(jan_first, BusinessDayConvention.none), "No adjustment.")
        
        # BusinessDayConvention.following
        self.assertEqual(jan_second, cal.adjust(jan_first, BusinessDayConvention.following), "Adjusted to January 2.")
    
if __name__ == "__main__":
    unittest.main()