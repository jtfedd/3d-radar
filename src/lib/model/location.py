from .geo_point import GeoPoint


class Location:
    def __init__(self, address: str, area: str, lat: float, lon: float):
        self.address = address
        self.area = area
        self.geoPoint = GeoPoint(lat, lon)

    def getLabel(self) -> str:
        return ", ".join([self.address, self.area])

    def getLabel2(self) -> str:
        return "\n".join([self.address, self.area])
