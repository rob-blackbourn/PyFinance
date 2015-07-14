class YearMonthDay(object):
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        
    def __str__(self):
        return "{0}-{1:02}-{2:02}".format(self.year, self.month, self.day)
    
    def __eq__(self, other):
        return isinstance(other, YearMonthDay) and self.year == other.year and self.month == other.month and self.day == other.day
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, YearMonthDay) and (self.years < other.years or self.months < other.months or self.days < other.days)
    
    def __le__(self, other):
        return isinstance(other, YearMonthDay) and (self.years <= other.years or self.months <= other.months or self.days <= other.days)
    
    def __gt__(self, other):
        return isinstance(other, YearMonthDay) and (self.years > other.years or self.months > other.months or self.days > other.days)
    
    def __ge__(self, other):
        return isinstance(other, YearMonthDay) and (self.years >= other.years or self.months >= other.months or self.days >= other.days)
        