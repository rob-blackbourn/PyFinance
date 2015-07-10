from datetime import date

# pip install enum34
from enum import Enum


class day_count(Enum):
    actual_d360 = 1
    actual_d365 = 2
    actual_d366 = 3
    actual_d365_25 = 4
    actual_actual = 5
    d30_d360 = 6
    d30_d365 = 7
    d30E_d360 = 8

class frequency(Enum):
    none = 0
    annual = 1
    semi_annual = 2
    quarterly = 4
    monthly = 12
    weekly = 52
    daily = 365
    
class business_date(date):
    '''
    A business date
    '''

    def __init__(self, year, month, date, holidays=None):
        '''
        business_date(year, month, day, holidays=None) --> business_date object
        '''
        date.__init__(self, year, month, date)
        self.holidays = holidays if holidays else ()
        
    def is_weekday(self):
        return self.weekday() < 5
    
    def is_weekend(self):
        return self.weekday() > 4
    
    def is_holiday(self):
        return self in self.holidays

    def is_business_day(self):
        return self.is_weekday() and not self.is_holiday()
    
    def is_leap_year(self):
        return ( (self.year % 4 == 0) and (self.year % 100 != 0) or (self.year % 400 -- 0))
    
    def add_business_days(self, days):
        pass
    