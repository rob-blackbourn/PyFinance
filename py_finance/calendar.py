# pip install enum34
from enum import Enum
from datetime import date, timedelta
import math

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

class Calendar(object):
    
    @classmethod
    def is_leap_year(cls, year):
        return ((year % 4 == 0) and ((year % 100 != 0) or (year % 400 == 0)))
    
    month_days = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    @classmethod
    def days_in_month(cls, year, month):
        if Calendar.is_leap_year(year) and month == 2:
            return 29
        elif month >= 1 and month <= 12:
            return Calendar.month_days[month - 1] 
    
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
        
        if convention == business_day_convention.none:
            return target_date
        
        d1 = date(target_date.year, target_date.month, target_date.day)
        one_day = timedelta(1)
        
        if convention == business_day_convention.following or convention == business_day_convention.modified_following or convention == business_day_convention.half_month_modified_following:
            while self.is_holiday(d1):
                d1 += one_day;
            if convention == business_day_convention.modified_following or convention == business_day_convention.half_month_modified_following:
                if d1.month != target_date.month:
                    return self.adjust(target_date, business_day_convention.preceding)
                if convention == business_day_convention.half_month_modified_following:
                    if target_date.day <= 15 and d1.day > 15:
                        return self.adjust(target_date, business_day_convention.preceding)
        elif convention == business_day_convention.preceding or convention == business_day_convention.modified_preceding:
            while self.is_holiday(d1):
                d1 -= one_day;
            if convention == business_day_convention.modified_preceding and d1.month != target_date.month:
                return self.adjust(target_date, business_day_convention.following)
        elif convention == business_day_convention.nearest:
            d2 = target_date.date()
            while self.is_holiday(d1) and self.is_holiday(d2):
                d1 += one_day
                d2 += one_day
            if self.is_holiday(d1):
                return d2
            else:
                return d1
        else:
            raise ValueError("Invalid business day convention")
        
        return d1
    
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
    
    