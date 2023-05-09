from lib.model.data_point import DataPoint
import numpy as np
import math


class Ray:
    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[0]
        azimuth = math.radians(header.az_angle)
        elevation = math.radians(header.el_angle)

        reflectivity_header = level2Ray[4][b"REF"][0]
        first = reflectivity_header.first_gate
        spacing = reflectivity_header.gate_width

        reflectivity = level2Ray[4][b"REF"][1]

        return cls(azimuth, elevation, first, spacing, reflectivity)

    def __init__(self, azimuth, elevation, first, spacing, reflectivityData):
        self.azimuth = azimuth
        self.elevation = elevation

        self.first = first
        self.spacing = spacing

        self.reflectivity = reflectivityData

    def range(self, i):
        return self.first + self.spacing * i

    def foreach(self, f):
        sin_az = math.sin(self.azimuth)
        cos_az = math.cos(self.azimuth)

        sin_el = math.sin(self.elevation)
        cos_el = math.cos(self.elevation)

        x_factor = cos_el * sin_az
        y_factor = cos_el * cos_az
        z_factor = sin_el

        for i, value in enumerate(self.reflectivity):
            if np.isnan(value):
                continue

            dist = self.range(i)
            x = dist * x_factor
            y = dist * y_factor
            z = dist * z_factor

            f(DataPoint(x, y, z, value))
