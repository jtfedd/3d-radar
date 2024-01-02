from typing import Any, Dict, List, Self

from .location import Location


class LocationQuery:
    @classmethod
    def fromJson(cls, json: Dict[str, Any]) -> Self:  # type: ignore
        search = json["search"]
        limit = json["limit"]
        jsonResult = json["result"]
        lastUsed = json["lastUsed"]
        result: List[Location] = []
        for location in jsonResult:
            result.append(Location.fromJson(location))

        return cls(search, limit, result, lastUsed)

    def toJson(self) -> Dict[str, Any]:  # type: ignore
        raw: Dict[str, Any] = {}  # type: ignore

        raw["search"] = self.search
        raw["limit"] = self.limit
        raw["result"] = []
        raw["lastUsed"] = self.lastUsed

        for location in self.result:
            raw["result"].append(location.toJson())

        return raw

    def __init__(self, search: str, limit: int, result: List[Location], lastUsed: int):
        self.search = search
        self.limit = limit
        self.result = result
        self.lastUsed = lastUsed


def compareLocationQueries(a: LocationQuery, b: LocationQuery) -> int:
    if a.search == b.search and a.limit == b.limit:
        return 0

    if a.search > b.search:
        return 1
    if a.search < b.search:
        return -1

    if a.limit > b.limit:
        return 1
    if a.limit < b.limit:
        return -1

    return 0
