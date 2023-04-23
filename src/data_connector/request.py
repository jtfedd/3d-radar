import os

class Request:
    def __init__(self, station, date, time):
        self.station = station
        self.date = date
        self.time = time

    def awsKey(self):
        return self.format('{1}/{2}/{3}/{0}/{0}{1}{2}{3}_{4}{5}{6}')

    def cacheKey(self):
        return self.format('{0}_{1}{2}{3}_{4}{5}{6}')

    def formatNumber(self, value):
        return '{:02}'.format(value)
    
    def year(self):
        return self.formatNumber(self.date.year)
    
    def month(self):
        return self.formatNumber(self.date.month)
    
    def day(self):
        return self.formatNumber(self.date.day)
    
    def hour(self):
        return self.formatNumber(self.time.hour)
    
    def minute(self):
        return self.formatNumber(self.time.minute)
    
    def second(self):
        return self.formatNumber(self.time.second)
    
    def format(self, fmt):
        return fmt.format(
            self.station,
            self.year(), 
            self.month(), 
            self.day(),
            self.hour(),
            self.minute(),
            self.second(),
        )
