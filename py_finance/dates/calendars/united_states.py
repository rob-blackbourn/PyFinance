from datetime import date, timedelta
from py_finance.dates.calendar import Calendar
from py_finance.dates.calendar_month import JulianMonth
from py_finance.dates.day_of_week import DayOfWeek
from py_finance.dates.yearly_calendar import YearlyCalendar

class UnitedStatesSettlement(YearlyCalendar):

    def __init__(self):
        YearlyCalendar.__init__(self, "US-Settlement")
    
    def fetch_holidays(self, year):
        self.__generate_holidays(year)
    
    @classmethod
    def __generate_holidays(cls, year):
        
        empty = Calendar()
        
        # New Year's Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.january, 1))
        
        # Martin Luther King's birthday (third Monday in January)
        yield Calendar.add_nth_day_of_week(date(year, JulianMonth.january, 1), 3, DayOfWeek.monday, False)
        
        # Washington's birthday (third Monday in February)
        yield Calendar.add_nth_day_of_week(date(year, JulianMonth.february, 1), 3, DayOfWeek.monday, False)
        
        # Memorial Day (last Monday in May)
        yield Calendar.add_nth_day_of_week(Calendar.end_of_month(year, JulianMonth.may), -1, DayOfWeek.monday, False)
        
        # Independence Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.july, 4))

        # Labor Day (first Monday in September)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.september, 1), 1, DayOfWeek.monday, False)

        # Columbus Day (second Monday in October)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.october, 1), 2, DayOfWeek.monday, False)

        # Veteran's Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.november, 11))

        # Thanksgiving Day (fourth Thursday in November)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.november, 1), 4, DayOfWeek.thursday, False)

        # Christmas (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.december, 25))

class UnitedStatesNyse(YearlyCalendar):
    
    def __init__(self):
        YearlyCalendar.__init__(self, "US-NYSE")
    
    def fetch_holidays(self, year):
        return YearlyCalendar.fetch_holidays(self, year)
    
    @classmethod
    def __generatte_holidays(cls, year):
        
        empty = Calendar()
        
        # New Year's Day (possibly moved to Monday if on Sunday)
        new_years_day = date(year, JulianMonth.january, 1)
        yield (new_years_day if new_years_day.weekday() != DayOfWeek.sunday else new_years_day + timedelta(1))
        
        # Washington's birthday (third Monday in February)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.february, 1), 3, DayOfWeek.monday, False)
        
        # Good Friday
        yield empty.easter(year) - timedelta(3)

        # Memorial Day (last Monday in May)
        yield empty.add_nth_day_of_week(empty.end_of_month(year, JulianMonth.may), -1, DayOfWeek.monday, False)

        # Independence Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.july, 4))

        # Labor Day (first Monday in September)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.september, 1), 1, DayOfWeek.monday, False)

        # Thanksgiving Day (fourth Thursday in November)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.november, 1), 4, DayOfWeek.thursday, False)

        # Christmas (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.december, 25))

        if year >= 1998:
            # Martin Luther King's birthday (third Monday in January)
            yield Calendar.add_nth_day_of_week(date(year, JulianMonth.january, 1), 3, DayOfWeek.monday, False)

        if year <= 1968 or (year <= 1980 and year % 4 == 0):
            # Presidential election days
            yield Calendar.add_nth_day_of_week(date(year, JulianMonth.november, 1), 1, DayOfWeek.tuesday, True)

        # Special closings
        if year == 2012:
            # Hurricane Sandy
            yield date(2012, JulianMonth.october, 29)
            yield date(2012, JulianMonth.october, 30)

        if year == 2007:
            # President Ford's funeral
            yield date(2007, JulianMonth.january, 2)
        
        if year == 2004:
            # President Reagan's funeral
            yield date(2004, JulianMonth.june, 11)
        
        if year == 2001:
            # September 11-14, 2001
            yield date(2001, JulianMonth.september, 11)
            yield date(2001, JulianMonth.september, 12)
            yield date(2001, JulianMonth.september, 13)
            yield date(2001, JulianMonth.september, 14)
            
        if year == 1994:
            # President Nixon's funeral
            yield date(1994, JulianMonth.april, 27)
            
        if year == 1985:
            # Hurricane Gloria
            yield date(1985, JulianMonth.september, 27)
            
        if year == 1977:
            # 1977 Blackout
            yield date(1977, JulianMonth.july, 14)
            
        if year == 1973:
            # Funeral of former President Lyndon B. Johnson.
            yield date(1973, JulianMonth.january, 25)
            
        if year == 1972:
            # Funeral of former President Harry S. Truman
            yield date(1972, JulianMonth.december, 28)
            
        if year == 1969:
            # National Day of Participation for the lunar exploration.
            yield date(1969, JulianMonth.july, 21)
            # Funeral of former President Eisenhower.
            yield date(1969, JulianMonth.march, 31)
            # Closed all day - heavy snow.
            yield date(1969, JulianMonth.february, 10)
            
        if year == 1968:
            # Day after Independence Day.
            yield date(1968, JulianMonth.july, 5)
            # June 12-Dec. 31, 1968
            # Four day week (closed on Wednesdays) - Paperwork Crisis
            d = date(1968, JulianMonth.june, 12)
            while d.year == 1968:
                yield d
                d += timedelta(7)
            # Day of mourning for Martin Luther King Jr.
            yield date(1968, JulianMonth.april, 9)
        
        if year == 1963:
            # Funeral of President Kennedy
            yield date(1963, JulianMonth.november, 25)
        
        if year == 1961:
            # Day before Decoration Day
            yield date(1961, JulianMonth.may, 29)
            
        if year == 1958:
            # Day after Christmas
            yield date(1958, JulianMonth.december, 26)
            
        if year == 1954 or year == 1956 or year == 1965:
            # Christmas Eve
            yield date(year, JulianMonth.december, 24)


class UnitedStatesGovernmentBond(YearlyCalendar):

    def __init__(self):
        YearlyCalendar.__init__(self, "US-GovtBond")
    
    def fetch_holidays(self, year):
        self.__generate_holidays(year)
    
    @classmethod
    def __generate_holidays(cls, year):
        
        empty = Calendar()
        
        # New Year's Day (possibly moved to Monday if on Sunday)
        new_years_day = date(year, JulianMonth.january, 1)
        yield (new_years_day if new_years_day.weekday() != DayOfWeek.sunday else new_years_day + timedelta(1))
        
        # Martin Luther King's birthday (third Monday in January)
        yield Calendar.add_nth_day_of_week(date(year, JulianMonth.january, 1), 3, DayOfWeek.monday, False)
        
        # Washington's birthday (third Monday in February)
        yield Calendar.add_nth_day_of_week(date(year, JulianMonth.february, 1), 3, DayOfWeek.monday, False)
        
        # Good Friday
        yield empty.easter(year) - timedelta(3)

        # Memorial Day (last Monday in May)
        yield Calendar.add_nth_day_of_week(Calendar.end_of_month(year, JulianMonth.may), -1, DayOfWeek.monday, False)
        
        # Independence Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.july, 4))

        # Labor Day (first Monday in September)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.september, 1), 1, DayOfWeek.monday, False)

        # Columbus Day (second Monday in October)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.october, 1), 2, DayOfWeek.monday, False)

        # Veteran's Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.november, 11))

        # Thanksgiving Day (fourth Thursday in November)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.november, 1), 4, DayOfWeek.thursday, False)

        # Christmas (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.december, 25))


class UnitedStatesNerc(YearlyCalendar):

    def __init__(self):
        YearlyCalendar.__init__(self, "US-NERC")
    
    def fetch_holidays(self, year):
        self.__generate_holidays(year)
    
    @classmethod
    def __generate_holidays(cls, year):
        
        empty = Calendar()
        
        # New Year's Day (possibly moved to Monday if on Sunday)
        new_years_day = date(year, JulianMonth.january, 1)
        yield (new_years_day if new_years_day.weekday() != DayOfWeek.sunday else new_years_day + timedelta(1))
        
        # Memorial Day (last Monday in May)
        yield Calendar.add_nth_day_of_week(Calendar.end_of_month(year, JulianMonth.may), -1, DayOfWeek.monday, False)
        
        # Independence Day (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.july, 4))

        # Labor Day (first Monday in September)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.september, 1), 1, DayOfWeek.monday, False)

        # Thanksgiving Day (fourth Thursday in November)
        yield empty.add_nth_day_of_week(date(year, JulianMonth.november, 1), 4, DayOfWeek.thursday, False)

        # Christmas (Monday if Sunday or Friday if Saturday)
        yield empty.nearest_business_day(date(year, JulianMonth.december, 25))
