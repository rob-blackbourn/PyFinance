class YearMonthDay(object):
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        
    def __str__(self):
        return "{0}-{1:02}-{2:02}".format(self.year, self.month, self.day)