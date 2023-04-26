from src.model.sweep import Sweep

class Scan:
    def __init__(self, level2File, station, date, time):
        self.station = station
        self.date = date
        self.time = time

        self.sweeps = []

        for sweep in level2File.sweeps:
            self.sweeps.append(Sweep(sweep))
    
    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)

    def points(self):
        points = []
        self.foreach(lambda p : points.append(p))
        return points