import numpy as np


class Scan:
    def __init__(self, sweeps, station, date, time):
        self.sweeps = sweeps
        self.station = station
        self.date = date
        self.time = time

        self.sweeps = sorted(self.sweeps, key=lambda sweep: sweep.elevation)

    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)

    def points(self):
        points = []
        self.foreach(lambda p: points.append(p))
        return points

    def reflectivityMatrix(self):
        sweeps = [sweep.reflectivityMatrix() for sweep in self.sweeps]
        return np.stack(sweeps)

    def getElevations(self):
        return [sweep.elevation for sweep in self.sweeps]

    def getAzimuths(self):
        return np.linspace(0, 359.5, 720)

    def getRanges(self):
        return np.linspace(
            self.sweeps[0].rays[0].first,
            self.sweeps[0].rays[0].first + 2000 * self.sweeps[0].rays[0].spacing,
            2001,
        )
