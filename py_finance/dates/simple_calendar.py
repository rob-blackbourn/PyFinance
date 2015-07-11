from py_finance.dates.calendar import Calendar

class SimpleCalendar(Calendar):
    
    def __init__(self, holidays = []):
        self.holidays = holidays
        
    def is_holiday(self, value):
        return value in self.holidays
