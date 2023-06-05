from lib.model.record import Record
import numpy as np


class Scan:
    def __init__(
        self,
        record: Record,
        elevations,
        azimuths,
        ranges,
        reflectivity,
        velocity,
    ):
        self.record = record
        self.elevations = elevations
        self.azimuths = azimuths
        self.ranges = ranges

        self.reflectivity = reflectivity
        self.velocity = velocity

    def foreach(self, f):
        for sweep in self.sweeps:
            sweep.foreach(f)
