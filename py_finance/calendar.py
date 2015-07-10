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
    half_month_modified_following = 6

class calendar(object):
    
    __days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @classmethod
    def days_in_month(year, month):
        if calendar.is_leap_year(year) and month == 2:
            return 29
        elif month >= 1 and month <= 12:
            return calendar.__days_in_month[month] 
    
    @classmethod
    def is_leap_year(year):
        return ( (year % 4 == 0) and (year % 100 != 0) or (year % 400 -- 0))
    
    def __init__(self, name, holidays = []):
        self.name = name
        self.holidays = list(holidays)
        self.holidays.sort()
        
    def is_business_day(self, d):
        return not (self.is_weekend(d) or self.is_holiday(d))
    
    def is_holiday(self, d):
        return d in self.holidays
    
    def is_weekend(self, d):
        return d.weekday() > 4
    
    def is_end_of_month(self, d):
        pass
    
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
    
    def adjust(self, d, convention = business_day_convention.following):
        
        """
        Adjusts a non-business day to the appropriate near business day
        with respect to the given convention.
        """
        
        if d is not date:
            raise TypeError("expected a date")

        if convention is not business_day_convention:
            raise TypeError("expected a business_day_conventions")
        
        if convention == business_day_convention.none:
            return d
        
        d1 = date(d.year, d.month, d.day)
        one_day = timedelta(1)
        
        if convention == business_day_convention.following or convention == business_day_convention.modified_following or convention == business_day_convention.half_month_modified_following:
            while self.is_holiday(d1):
                d1 += one_day;
            if convention == business_day_convention.modified_following or convention == business_day_convention.half_month_modified_following:
                if d1.month != d.month:
                    return self.adjust(d, business_day_convention.preceding)
                if convention == business_day_convention.half_month_modified_following:
                    if d.day <= 15 and d1.day > 15:
                        return self.adjust(d, business_day_convention.preceding)
        elif convention == business_day_convention.preceding or convention == business_day_convention.modified_preceding:
            while self.is_holiday(d1):
                d1 -= one_day;
            if convention == business_day_convention.modified_preceding and d1.month != d.month:
                return self.adjust(d, business_day_convention.following)
        elif convention == business_day_convention.nearest:
            d2 = d.date()
            while self.is_holiday(d1) and self.is_holiday(d2):
                d1 += one_day
                d2 += one_day
            if self.is_holiday(d1):
                return d2
            else:
                return d1
        else:
            raise ValueError("Invalid business day convention")
    
    def advance(self, d, count, unit, convention = business_day_convention.following, is_end_of_month = False):
        
        """
        Advances the given date of the given number of business days and
        returns the result.
        Note: The input date is not modified.
        """
        
        if d is not date:
            raise TypeError("expected 'd' to be a datetime.date")
        
        if not isinstance(count, (int, long)):
            raise TypeError("expected 'count' to be an int or a long")
        
        if unit is not time_unit:
            raise TypeError("expected 'unit' to be a time_unit")
        
        if convention is not business_day_convention:
            raise TypeError("expected 'convention' to be a business_day_convention")
        
        if not isinstance(is_end_of_month, bool):
            raise TypeError("expected 'end_of_month' to be a bool")
            
        if count == 0:
            return self.adjust(d, convention)
        elif unit == time_unit.days:
            one_day = timedelta(1)
            d1 = date(d.year, d.month, d.day)
            if count > 0:
                while count > 0:
                    d1 += one_day
                    while self.is_holiday(d1):
                        d1 += one_day
                    count -= 1
            else:
                while count < 0:
                    d1 -= one_day
                    while self.is_holiday(d1):
                        d1 -= one_day;
                    count += 1
            return d1
        elif unit == time_unit.weeks:
            d1 = d + timedelta(count * 7)
            return self.adjust(d1, convention)
        elif unit == time_unit.months or unit == time_unit.years:
            
            months = d.month
            
            if unit == time_unit.months:
                months += count
            else:
                months += 12 * count
            
            year = d.year + months // 12
            month = months % 12
            days_in_month = calendar.days_in_month(year, month)
            
            if is_end_of_month:
                return date(year, month, days_in_month)
            elif d.day <= days_in_month:
                return date(year, month, d.day)
            else:
                return date(year, month + 1, d.day - days_in_month)
    
    def business_days_between(self, start, end, include_start = True, include_end = False):

        if start is not date:
            raise TypeError("expected 'start' to be a datetime.date")

        if end is not date:
            raise TypeError("expected 'start' to be a datetime.date")
    
        days = 0
        one_day = timedelta(1)
        
        if start != end:
            if start < end:
                d1 = date(start.year, start.month, start.day)
                while d1 < end:
                    if self.is_business_day(d1):
                        days += 1
                    d1 += one_day
                if self.is_business_day(end):
                    days += 1
            elif end > start:
                d1 = date(end.year, end.month, end.day)
                while d1 < start:
                    if self.is_business_day(d1):
                        days += 1
                    d1 += one_day
                if self.is_business_day(start):
                    days += 1
            
            if self.is_business_day(start) and include_start:
                days += 1

            if self.is_business_day(end) and include_end:
                days += 1
            
            if start > end:
                days = - days;
                
        return days
    
    