class RayHeader:
    @classmethod
    def fromLevel2Data(cls, level2Ray):
        header = level2Ray[0]
        return cls(header.az_angle, header.el_angle)

    def __init__(self, azimuth, elevation):
        self.azimuth = azimuth
        self.elevation = elevation