import json
import time
from functools import cmp_to_key
from pathlib import Path
from typing import List

from lib.app.files.manager import FileManager
from lib.model.location import Location
from lib.model.location_query import LocationQuery, compareLocationQueries
from lib.network.network import Network


class LocationService:
    CACHE_SIZE = 100

    def __init__(self, fileManager: FileManager, network: Network) -> None:
        self.fileManager = fileManager
        self.network = network

        self.cache: List[LocationQuery] = []
        self.prepopulateCache()

    def search(self, address: str, limit: int = 1) -> List[Location] | None:
        cachedResult = self.searchCache(address, limit)
        if cachedResult:
            cachedResult.lastUsed = int(time.time())
            return cachedResult.result

        locations = self.network.locations.search(address, limit)
        if not locations:
            return None

        self.cache.append(LocationQuery(address, limit, locations, int(time.time())))
        self.reformatCache()

        return locations

    def searchCache(self, address: str, limit: int) -> LocationQuery | None:
        key = LocationQuery(address, limit, [], 0)
        index = self.binarySearch(key, 0, len(self.cache) - 1)

        if index < 0:
            return None

        return self.cache[index]

    def binarySearch(self, key: LocationQuery, left: int, right: int) -> int:
        while left <= right:
            mid = (left + right) // 2

            if compareLocationQueries(self.cache[mid], key) == 0:
                return mid

            if compareLocationQueries(self.cache[mid], key) < 0:
                left = mid + 1
            else:
                right = mid - 1

        return -1

    def reformatCache(self) -> None:
        if len(self.cache) > self.CACHE_SIZE:
            self.cache.sort(key=lambda q: q.lastUsed, reverse=True)
            self.cache = self.cache[: self.CACHE_SIZE]

        self.cache.sort(key=cmp_to_key(compareLocationQueries))

    def getCacheFile(self) -> Path:
        return self.fileManager.getCacheFile("locations.json")

    def prepopulateCache(self) -> None:
        filePath = self.getCacheFile()

        if not filePath.exists():
            return

        print("Reading", filePath)

        with filePath.open("r", encoding="utf-8") as file:
            raw = file.read()
            if len(raw) == 0:
                return

            locationJson = json.loads(raw)
            for locationQuery in locationJson:
                self.cache.append(LocationQuery.fromJson(locationQuery))

        self.reformatCache()

    def writeCacheFile(self) -> None:
        filePath = self.getCacheFile()

        print("Writing", filePath)

        with filePath.open("w", encoding="utf-8") as file:
            raw = []

            for locationQuery in self.cache:
                raw.append(locationQuery.toJson())

            rawJson = json.dumps(
                raw,
                indent=4,
            )

            file.write(rawJson)

    def destroy(self) -> None:
        self.writeCacheFile()
