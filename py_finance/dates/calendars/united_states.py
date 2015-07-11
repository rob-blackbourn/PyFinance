from py_finance.dates.calendar import YearlyCalendar, calendar_month, day_of_week,\
    Calendar
from datetime import date

class UnitedStatesSettlement(YearlyCalendar):

    def __init__(self, params):
        YearlyCalendar.__init__(self, "US-Settlement")
    
    def fetch_holidays(self, year):
        
        holidays = []
        
        # New Year's Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, calendar_month.january, 1)))
        
        # Martin Luther King's birthday (third Monday in January)
        holidays.append(Calendar.add_nth_day_of_week(date(year, calendar_month.january, 1), 3, day_of_week.monday, False))
        
        # Washington's birthday (third Monday in February)
        holidays.append(Calendar.add_nth_day_of_week(date(year, calendar_month.february, 1), 3, day_of_week.monday, False))
        
        # Memorial Day (last Monday in May)
        holidays.append(Calendar.add_nth_day_of_week(Calendar.end_of_month(year, calendar_month.may), -1, day_of_week.monday, False))
        
        # Independence Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, calendar_month.july, 4)))

        # Labor Day (first Monday in September)
        holidays.append(self.add_nth_day_of_week(date(year, calendar_month.september, 1), 1, day_of_week.monday, False))

        # Columbus Day (second Monday in October)
        holidays.append(self.add_nth_day_of_week(date(year, calendar_month.october, 1), 2, day_of_week.monday, False))

        # Veteran's Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, calendar_month.november, 11)))

        # Thanksgiving Day (fourth Thursday in November)
        holidays.append(self.add_nth_day_of_week(date(year, calendar_month.november, 1), 4, day_of_week.thursday, False))

        # Christmas (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, calendar_month.december, 25)))
        
        return holidays
