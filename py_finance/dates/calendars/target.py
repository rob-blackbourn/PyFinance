from datetime import timedelta, date
from py_finance.dates.business_day_convention import BusinessDayConvention
from py_finance.dates.yearly_calendar import YearlyCalendar
from py_finance.dates.calendar import Calendar

class Target(YearlyCalendar):

    def __init__(self, params):
        YearlyCalendar.__init__(self, "TARGET")

    def fetch_holidays(self, year):
        self.__generate_holidays(year)
    
    @classmethod
    def __generate_holidays(cls, year):
        
        empty = Calendar()
        
        # New Year's Day
        yield empty.adjust(date(year, 1, 1), BusinessDayConvention.following)
        
        if year >= 2000:
            # Good Friday and Easter Monday
            easter_monday = empty.easter(year);
            yield easter_monday + timedelta(-3)
            yield easter_monday
            
        if year >= 2000:
            # Labour Day
            yield date(year, 5, 1)

        # Christmas
        yield date(year, 12, 25)

        if year >= 2000:
            # Day of Goodwill
            yield date(year, 12, 26)

        if year == 1998 or year == 1999 or year == 2001:
            yield date(year, 12, 31)
