from .geo_point import GeoPoint


class Location:
    def __init__(self, address: str, area: str, lat: float, lon: float):
        self.address = address
        self.area = area
        self.geoPoint = GeoPoint(lat, lon)

    def getLabel(self) -> str:
        return self.makeLabel(", ")

    def getLabel2(self) -> str:
        return self.makeLabel("\n")

    def makeLabel(self, sep: str) -> str:
        if len(self.address) == 0:
            return self.area
        if len(self.area) == 0:
            return self.address
        return sep.join([self.address, self.area])
