from py_calendrical.utils import reduce_cond

class YearMonthDay(object):
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    def to_tuple(self):
        return (self.year, self.month, self.day)
    
    def __str__(self):
        return "{0}-{1:02}-{2:02}".format(self.year, self.month, self.day)
    
    def __eq__(self, other):
        return isinstance(other, YearMonthDay) and all(map(lambda (x,y): x == y, zip(self.to_tuple(), other.to_tuple())))
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        return isinstance(other, YearMonthDay) and reduce_cond(lambda _, (x, y): x < y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __le__(self, other):
        return isinstance(other, YearMonthDay) and reduce_cond(lambda _, (x, y): x <= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __gt__(self, other):
        return isinstance(other, YearMonthDay) and reduce_cond(lambda _, (x, y): x > y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
    
    def __ge__(self, other):
        return isinstance(other, YearMonthDay) and reduce_cond(lambda _, (x, y): x >= y, lambda r, (x, y): not r and x == y, zip(self.to_tuple(), other.to_tuple()), False)
        