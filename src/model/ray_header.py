class RayHeader:
    def __init__(self, level2Ray):
        header = level2Ray[0]
        self.azimuth = header.az_angle
        self.elevation = header.el_angle