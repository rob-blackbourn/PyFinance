from datetime import date, timedelta
from py_finance.dates.business_day_convention import BusinessDayConvention
from py_finance.dates.day_of_week import DayOfWeek
from py_finance.dates.yearly_calendar import YearlyCalendar

class UnitedKingdom(YearlyCalendar):

    def __init__(self, params):
        YearlyCalendar.__init__(self, "UK")
    
    def fetch_holidays(self, year):
        
        holidays = []
        
        # New Years Days, adjusted to the first non-weekend.
        holidays.append(self.adjust(date(year, 1, 1), BusinessDayConvention.following))

        # Easter Monday
        easter_monday = self.easter(year)
        holidays.append(easter_monday)
        # Good Friday
        holidays.append(easter_monday + timedelta(-3))

        if year == 2011:
            # Royal Wedding
            holidays.append(date(2011, 4, 29))
            
        # May Day - first Monday in May.
        holidays.append(self.add_nth_day_of_week(date(year, 5, 1), 1, DayOfWeek.monday, False))
        
        if year == 2002:
            # Golden Jubilee Bank Holiday
            holidays.append(date(2002, 6, 3))
            # Special Spring Bank Holiday
            holidays.append(date(2002, 6, 4))
        elif year == 2012:
            # Diamond Jubilee Bank Holiday
            holidays.append(date(2012, 6, 4))
            # Special Spring Bank Holiday
            holidays.append(date(2012, 6, 5))
        else:
            # Spring Bank Holiday - last Monday in May
            holidays.append(self.add_nth_day_of_week(self.end_of_month(year, 5), -1, DayOfWeek.monday, False))
        
        # August Bank Holiday - last Monday in August.
        holidays.append(self.add_nth_day_of_week(self.end_of_month(year, 8), -1, DayOfWeek.monday, False))

        # Christmas Day        
        christmas_day = self.adjust(date(year, 12, 25), BusinessDayConvention.following)
        holidays.append(christmas_day)
        # Boxing Day
        holidays.append(self.add_business_days(christmas_day, 1))
        
        if year == 1999:
            # Millennium Celebration
            holidays.append(date(1999, 12, 31))
            
        holidays.sort()
        
        return holidays
        
