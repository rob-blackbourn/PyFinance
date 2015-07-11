from py_finance.dates.calendar import Calendar

class YearlyCalendar(Calendar):
    
    def __init__(self, name):
        self.__years_fetched = set()
        self.__holidays = set()
        
    def is_holiday(self, target_date):
        
        if not self.__is_cached(target_date.year):
            self.__cache_holidays(target_date.year)

        return target_date in self.__holidays

    def fetch_holidays(self, year):
        return []

    def __is_cached(self, year):
        return year in self.__years_fetched
    
    def __cache_holidays(self, year):
        for holiday in self.fetch_holidays(year):
            self.__holidays.add(holiday)
        self.__years_fetched.add(year)
