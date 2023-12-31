from .geo_point import GeoPoint


class RadarStation:
    def __init__(self, stationID: str, name: str, lat: float, lon: float):
        self.stationID = stationID
        self.name = name
        self.geoPoint = GeoPoint(lat, lon)
