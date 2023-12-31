from .geo_point import GeoPoint


class Location:
    def __init__(self, name: str, lat: float, lon: float):
        self.name = name
        self.geoPoint = GeoPoint(lat, lon)
