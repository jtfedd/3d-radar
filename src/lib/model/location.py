from typing import Any, Dict, Self

from .geo_point import GeoPoint


class Location:
    @classmethod
    def fromJson(cls, json: Dict[str, Any]) -> Self:  # type: ignore
        address = json["address"]
        area = json["area"]
        lat = json["lat"]
        lon = json["lon"]

        return cls(address, area, lat, lon)

    def toJson(self) -> Dict[str, Any]:  # type: ignore
        raw: Dict[str, Any] = {}  # type: ignore

        raw["address"] = self.address
        raw["area"] = self.area
        raw["lat"] = self.geoPoint.lat
        raw["lon"] = self.geoPoint.lon

        return raw

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
