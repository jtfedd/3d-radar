from lib.model.data_point import DataPoint
import numpy as np
import math


class Ray:
    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[0]
        azimuth = math.radians(header.az_angle)

        reflectivity_header = level2Ray[4][b"REF"][0]
        first = reflectivity_header.first_gate
        spacing = reflectivity_header.gate_width

        reflectivity = level2Ray[4][b"REF"][1]

        # TODO this is a bit of a hack to make all of the rays the same length.
        # This should be cleaned up later
        reflectivity = np.pad(
            reflectivity,
            (1, 2000 - reflectivity.shape[0]),
            mode="constant",
            constant_values=(np.nan),
        )

        # Account for the nan added to the start of the reflectivity list
        first = first - spacing

        return cls(azimuth, first, spacing, reflectivity)

    def __init__(self, azimuth, first, spacing, reflectivityData):
        self.azimuth = azimuth
        self.first = first
        self.spacing = spacing
        self.reflectivity = reflectivityData

    def range(self, i):
        return self.first + self.spacing * i

    def foreach(self, elevation, f):
        azimuth = self.azimuth

        sin_az = math.sin(azimuth)
        cos_az = math.cos(azimuth)

        sin_el = math.sin(elevation)
        cos_el = math.cos(elevation)

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
