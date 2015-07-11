from datetime import date, timedelta
from py_finance.dates.business_day_convention import BusinessDayConvention
from py_finance.dates.day_of_week import DayOfWeek
from py_finance.dates.yearly_calendar import YearlyCalendar
from py_finance.dates.calendar_month import CalendarMonth
from py_finance.dates.calendar import Calendar

class UnitedKingdom(YearlyCalendar):

    def __init__(self):
        YearlyCalendar.__init__(self, "UK")
        
    def fetch_holidays(self, year):
        return self.__generate_holidays(year)
    
    @classmethod
    def __generate_holidays(cls, year):
        
        empty = Calendar();
        
        # New Years Days, adjusted to the first non-weekend.
        yield empty.adjust(date(year, CalendarMonth.january, 1), BusinessDayConvention.following)

        # Good Friday and Easter Monday
        easter_monday = empty.easter(year)
        yield easter_monday - timedelta(3)
        yield easter_monday

        if year == 2011:
            # Royal Wedding
            yield date(2011, CalendarMonth.april, 29)
            
        # May Day - first Monday in May.
        yield empty.add_nth_day_of_week(date(year, CalendarMonth.may, 1), 1, DayOfWeek.monday, False)
        
        if year == 2002:
            # Golden Jubilee Bank Holiday
            yield date(2002, CalendarMonth.june, 3)
            # Special Spring Bank Holiday
            yield date(2002, CalendarMonth.june, 4)
        elif year == 2012:
            # Diamond Jubilee Bank Holiday
            yield date(2012, CalendarMonth.june, 4)
            # Special Spring Bank Holiday
            yield date(2012, CalendarMonth.june, 5)
        else:
            # Spring Bank Holiday - last Monday in May
            yield empty.add_nth_day_of_week(empty.end_of_month(year, CalendarMonth.may), -1, DayOfWeek.monday, False)
        
        # August Bank Holiday - last Monday in August.
        yield empty.add_nth_day_of_week(empty.end_of_month(year, CalendarMonth.august), -1, DayOfWeek.monday, False)

        # Christmas Day
        christmas_day = empty.adjust(date(year, CalendarMonth.december, 25), BusinessDayConvention.following)
        yield christmas_day

        # Boxing Day
        yield empty.add_business_days(christmas_day, 1)
        
        if year == 1999:
            # Millennium Celebration
            yield date(1999, CalendarMonth.december, 31)

    
