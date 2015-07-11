from datetime import date
from py_finance.dates.calendar import Calendar
from py_finance.dates.calendar_month import CalendarMonth
from py_finance.dates.day_of_week import DayOfWeek
from py_finance.dates.yearly_calendar import YearlyCalendar

class UnitedStatesSettlement(YearlyCalendar):

    def __init__(self, params):
        YearlyCalendar.__init__(self, "US-Settlement")
    
    def fetch_holidays(self, year):
        
        holidays = []
        
        # New Year's Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, CalendarMonth.january, 1)))
        
        # Martin Luther King's birthday (third Monday in January)
        holidays.append(Calendar.add_nth_day_of_week(date(year, CalendarMonth.january, 1), 3, DayOfWeek.monday, False))
        
        # Washington's birthday (third Monday in February)
        holidays.append(Calendar.add_nth_day_of_week(date(year, CalendarMonth.february, 1), 3, DayOfWeek.monday, False))
        
        # Memorial Day (last Monday in May)
        holidays.append(Calendar.add_nth_day_of_week(Calendar.end_of_month(year, CalendarMonth.may), -1, DayOfWeek.monday, False))
        
        # Independence Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, CalendarMonth.july, 4)))

        # Labor Day (first Monday in September)
        holidays.append(self.add_nth_day_of_week(date(year, CalendarMonth.september, 1), 1, DayOfWeek.monday, False))

        # Columbus Day (second Monday in October)
        holidays.append(self.add_nth_day_of_week(date(year, CalendarMonth.october, 1), 2, DayOfWeek.monday, False))

        # Veteran's Day (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, CalendarMonth.november, 11)))

        # Thanksgiving Day (fourth Thursday in November)
        holidays.append(self.add_nth_day_of_week(date(year, CalendarMonth.november, 1), 4, DayOfWeek.thursday, False))

        # Christmas (Monday if Sunday or Friday if Saturday)
        holidays.append(self.nearest_business_day(date(year, CalendarMonth.december, 25)))
        
        return holidays