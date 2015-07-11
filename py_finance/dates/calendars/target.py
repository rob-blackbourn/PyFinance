from py_finance.dates.calendar import YearlyCalendar, business_day_convention
from datetime import timedelta, date

class Target(YearlyCalendar):

    def __init__(self, params):
        YearlyCalendar.__init__(self, "TARGET")

    def fetch_holidays(self, year):
        holidays = []
        
        # New Year's Day
        holidays.append(self.adjust(date(year, 1, 1), business_day_convention.following))
        
        if year >= 2000:
            # Good Friday and Easter Monday
            easter_monday = self.easter(year);
            holidays.append(easter_monday + timedelta(-3))
            holidays.append(easter_monday)
            
        if year >= 2000:
            # Labour Day
            holidays.append(date(year, 5, 1))

        # Christmas
        holidays.append(date(year, 12, 25))

        if year >= 2000:
            # Day of Goodwill
            holidays.append(date(year, 12, 26))

        if year == 1998 or year == 1999 or year == 2001:
            holidays.append(date(year, 12, 31))

        holidays.sort()

        return holidays
        