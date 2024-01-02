from typing import List

from .location import Location


class LocationQuery:
    def __init__(self, search: str, limit: int, result: List[Location]):
        self.search = search
        self.limit = limit
        self.result = result


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
