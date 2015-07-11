from py_finance.dates.calendar import Calendar

class YearlyCalendar(Calendar):
    
    def __init__(self, name):
        self.__years_fetched = set()
        self.__holidays = set()
        
    def is_holiday(self, target_date):
        
        if target_date.year not in self.__years_fetched:
            for holiday in self.fetch_holidays(target_date.year):
                self.__holidays.add(holiday)
            self.__years_fetched.add(target_date.year)

        return Calendar.is_holiday(self, target_date)

    def fetch_holidays(self, year):
        return []
