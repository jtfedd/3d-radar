from lib.model.sweep import Sweep


class Scan:
    @classmethod
    def fromLevel2Data(cls, level2File, station, date, time):
        sweeps = []

        for sweep in level2File.sweeps:
            sweeps.append(Sweep.fromLevel2Data(sweep))

        return cls(sweeps, station, date, time)

    def __init__(self, sweeps, station, date, time):
        self.sweeps = sweeps
        self.station = station
        self.date = date
        self.time = time

    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)

    def points(self):
        points = []
        self.foreach(lambda p: points.append(p))
        return points
