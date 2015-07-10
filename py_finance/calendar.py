# pip install enum34
from enum import Enum
from datetime import date, timedelta

class time_unit(Enum):
    days = 0
    weeks = 1
    months = 2
    years = 3
    
class business_day_convention (Enum):
    none = 0
    nerarest = 1
    preceding = 2
    following = 3
    modified_preceding = 4
    modified_following = 5

class Calendar(object):
    
    @classmethod
    def is_leap_year(cls, year):
        return ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)))
    
    month_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @classmethod
    def days_in_month(cls, year, month):
        return 29 if Calendar.is_leap_year(year) and month == 2 else Calendar.month_days[month - 1] 
    
    @classmethod
    def days_in_year(cls, year):
        return 366 if Calendar.isLeapYear(year) else 365

    @classmethod
    def is_weekend(cls, value):
        return value.weekday() > 4

    @classmethod    
    def is_end_of_month(cls, value):
        return value.day == Calendar.days_in_month(value.year, value.month)

    @classmethod
    def add_months(cls, target_date, months, end_of_month = False):
        
        if months == 0:
            return target_date
        
        month = target_date.month + months;
        year = target_date.year

        if months > 0:
            year += month // 12
            month = month % 12
        else:
            if month <= 0:
                year += -month // 12 - 1
                month %= 12

        days_in_month = Calendar.days_in_month(year, month)
    
        if end_of_month and Calendar.is_end_of_month(target_date):
            return date(year, month, days_in_month)
        else:
            return date(year, month, min(target_date.day, days_in_month))
    
    @classmethod
    def end_of_month(cls, target_date):
        return date(target_date.year, target_date.month, Calendar.days_in_month(target_date.year, target_date.month))
    
    @classmethod
    def easter(cls, year):
        # Note: Only true for Gregorian dates

        y = year
        g = (y - ((y // 19) * 19)) + 1
        c = (y // 100) + 1
        x = ((3 * c) // 4) - 12
        z = (((8 * c) + 5) // 25) - 5
        d = ((5 * y) // 4) - x - 10
        e1 = (11 * g) + 20 + z - x
        e = e1 - ((e1 // 30) * 30)

        # The value of 'e' may be negative. The case of year = 14250, e.g.,
        # produces values of g = 1, z = 40 and x = 95. The value of e1 is thus
        # -24, and the 'mod' code fails to return the proper positive result.
        # The following correction produces a positive value, mod 30, for 'e'.
          
        while e < 0:
            e += 30
       
        if ((e == 25) and (g > 11)) or (e == 24L):
            e += 1;

        n = 44 - e;

        if n < 21:
            n += 30
      
        dpn = d + n
        n1 = dpn - ((dpn // 7) * 7)   
        n = n + 7 - n1;

        if n > 31:
            month = 4;
            day = n - 31;
        else:
            month = 3;
            day = n;
       
        return date(year, month, day)
    
    def __init__(self, name, holidays = []):
        self.name = name
        self.holidays = list(holidays)
        self.holidays.sort()
    
    def is_holiday(self, value):
        return value in self.holidays
        
    def is_business_day(self, value):
        return not (Calendar.is_weekend(value) or self.is_holiday(value))
    
    def add_holiday(self, d):
        self.holidays.append(d)
        self.holidays.sort()
    
    def remove_holiday(self, d):
        self.holidays.remove(d)
        self.holidays.sort()
    
    def holidays(self, start, end):
        for d in self.holidays:
            if d > end:
                break
            elif d > start:
                yield d
    
    def adjust(self, target_date, convention = business_day_convention.following):
        
        """
        Adjusts a non-business day to the appropriate near business day
        with respect to the given convention.
        """
        
        if convention == business_day_convention.none or self.is_business_day(target_date):
            return target_date
        elif convention == business_day_convention.following:
            return self.add_business_days(target_date, 1)
        elif convention == business_day_convention.preceding:
            return self.add_business_days(target_date, -1)
        elif convention == business_day_convention.modified_following:
            adjusted_date = self.add_business_days(target_date, 1)
            
            if adjusted_date.month == target_date.month:
                return adjusted_date
            else:
                return self.add_business_days(target_date, -1)
        elif convention == business_day_convention.modified_preceding:
            adjusted_date = self.add_business_days(target_date, -1)
            
            if adjusted_date.month == target_date.month:
                return adjusted_date
            else:
                return self.add_business_days(target_date, 1)
        else:
            raise ValueError("Invalid business day convention")
    
    def add_business_days(self, target_date, count):
        
        sign = 1 if count > 0 else -1
        signed_day = timedelta(sign)
        
        while count != 0:
            target_date += signed_day;
            count -= sign
            
            while not self.is_business_day(target_date):
                target_date += signed_day
        
        return target_date

    def add_weeks(self, target_date, count, convention = business_day_convention.following):
            d1 = target_date + timedelta(count * 7)
            return self.adjust(d1, convention)
                
    def advance(self, target_date, count, unit, convention = business_day_convention.following, end_of_month = False):
        
        """
        Advances the given date of the given number of business days and
        returns the result.
        Note: The input date is not modified.
        """
            
        if count == 0:
            return self.adjust(target_date, convention)
        elif unit == time_unit.days:
            return self.add_business_days(target_date, count)
        elif unit == time_unit.weeks:
            return self.add_weeks(target_date, count, convention)
        elif unit == time_unit.months:
            return self.adjust(Calendar.add_months(target_date, count, end_of_month), convention)
        elif unit == time_unit.years:
            return self.adjust(Calendar.add_months(target_date, 12 * count, end_of_month), convention)
        else:
            raise ValueError("Unhandled time_unit")
        
    def business_day_count(self, start, end):

        if start > end:
            return self.business_days_between(end, start)
        else:
            days = 0
            one_day = timedelta(1)
            target_date = date(start.year, start.month, start.day)
            while start < end:
                while not self.is_business_day(target_date):
                    target_date += one_day
                target_date += one_day
                days += 1
            return days
    
    