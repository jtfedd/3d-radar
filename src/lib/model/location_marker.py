from typing import Any, Dict, Self

from lib.util.uuid import uuid

from .location import Location


class LocationMarker:
    @classmethod
    def fromJson(cls, json: Dict[str, Any]) -> Self:  # type: ignore
        location = Location.fromJson(json["location"])
        visible = json["visible"]

        return cls(location, visible)

    def toJson(self) -> Dict[str, Any]:  # type: ignore
        raw: Dict[str, Any] = {}  # type: ignore

        raw["location"] = self.location.toJson()
        raw["visible"] = self.visible

        return raw

    def __init__(self, location: Location, visible: bool) -> None:
        self.location = location
        self.visible = visible
        self.id = uuid()
