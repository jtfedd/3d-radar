import datetime
import json
from pathlib import Path
from typing import Dict

from direct.stdpy import threading
from platformdirs import user_cache_dir, user_config_dir

from lib.app.events import AppEvents
from lib.app.files.serialization import SERIALIZATION_VERSION
from lib.app.state import AppState
from lib.util.events.listener import Listener


class CacheFileInfo:
    def __init__(self, size: int, lastAccess: int) -> None:
        self.size = size
        self.lastAccess = lastAccess


class FileManager(Listener):
    appName = "Stormfront"
    BYTES_PER_MEGABYTE = 1048576

    def __init__(self, state: AppState, events: AppEvents) -> None:
        super().__init__()

        self.state = state

        self.lock = threading.Lock()

        self._configPath = Path(
            user_config_dir(self.appName, False, ensure_exists=True)
        )
        self._cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))

        print("Config", self._configPath.absolute())
        print("Cache", self._cachePath.absolute())

        self.cacheMeta: Dict[str, CacheFileInfo] = {}

        self.allowSave = True

        self.init()
        self.listen(self.state.maxCacheSize, lambda _: self.resizeCache())
        self.listen(
            self.state.useCache, lambda value: self.clearCache() if not value else None
        )
        self.listen(events.clearCache, lambda _: self.clearCache())

    def init(self) -> None:
        with self.lock:
            self._initializeCacheMeta()

            if self.state.serializationVersion.value != SERIALIZATION_VERSION:
                self._clearCache()

    def readConfigFile(self) -> bytes | None:
        with self.lock:
            return self._readConfigFile()

    def saveConfigFile(self, data: bytes) -> None:
        with self.lock:
            return self._saveConfigFile(data)

    def readCacheFile(self, filename: str) -> bytes | None:
        with self.lock:
            return self._readCacheFile(filename)

    def saveCacheFile(self, filename: str, data: bytes) -> None:
        with self.lock:
            return self._saveCacheFile(filename, data)

    def clearCache(self) -> None:
        with self.lock:
            self._clearCache()

    def clearAllData(self) -> None:
        with self.lock:
            for file in self._cachePath.iterdir():
                file.unlink()
            self._cachePath.rmdir()

            for file in self._configPath.iterdir():
                file.unlink()
            self._configPath.rmdir()

            self.cacheMeta = {}
            self._recalculateCacheSize()

            self.allowSave = False

    def resizeCache(self) -> None:
        with self.lock:
            self._reduceCache(0)

    def destroy(self) -> None:
        super().destroy()

        with self.lock:
            self._saveFileAccessMeta()
            self.allowSave = False

    def _getConfigFilePath(self) -> Path:
        return self._configPath.joinpath("config.json")

    def _getCacheFilePath(self, filename: str) -> Path:
        return self._cachePath.joinpath(filename)

    def _makeTimestamp(self) -> int:
        return int(datetime.datetime.now(datetime.UTC).timestamp())

    def _maxCacheSize(self) -> int:
        return self.state.maxCacheSize.value * self.BYTES_PER_MEGABYTE

    def _recalculateCacheSize(self) -> None:
        size = 0

        for info in self.cacheMeta.values():
            size += info.size

        self.state.cacheSize.setValue(size)

    def _initializeCacheMeta(self) -> None:
        fileAccessMeta = self._loadFileAccessMeta()

        for p in self._cachePath.iterdir():
            stat = p.stat()
            size = stat.st_size
            time = (
                fileAccessMeta[p.name]
                if p.name in fileAccessMeta
                else self._makeTimestamp()
            )

            self.cacheMeta[p.name] = CacheFileInfo(
                size,
                time,
            )

        self._recalculateCacheSize()
        self._reduceCache(0)

    def _loadFileAccessMeta(self) -> Dict[str, int]:
        meta: Dict[str, int] = {}

        raw = self._readCacheFile("cacheMeta.json")

        if raw is None or len(raw) == 0:
            return meta

        metaJson = json.loads(raw)
        for filename in metaJson:
            meta[filename] = metaJson[filename]

        return meta

    def _saveFileAccessMeta(self) -> None:
        meta: Dict[str, int] = {}

        for entry in self.cacheMeta.items():
            meta[entry[0]] = entry[1].lastAccess

        rawJson = json.dumps(
            meta,
            indent=4,
        )

        rawBytes = rawJson.encode()

        self._saveCacheFile("cacheMeta.json", rawBytes)

    def _clearCache(self) -> None:
        for file in self._cachePath.iterdir():
            self._removeCacheFile(file)

    def _removeCacheFile(self, file: Path) -> None:
        if not file.exists():
            return

        print("Removing", str(file))
        file.unlink()

        if file.name in self.cacheMeta:
            del self.cacheMeta[file.name]

        self._recalculateCacheSize()

    def _readCacheFile(self, filename: str) -> bytes | None:
        if not self.state.useCache.value:
            return None

        filepath = self._getCacheFilePath(filename)
        print("Reading from cache", filename)

        if filename in self.cacheMeta:
            self.cacheMeta[filename].lastAccess = self._makeTimestamp()

        return self._readFile(filepath)

    def _saveCacheFile(self, filename: str, data: bytes) -> None:
        if not self.state.useCache.value:
            return

        print("Writing to cache", filename)

        if len(data) > self._maxCacheSize():
            return

        spaceNeeded = len(data) - (
            self.cacheMeta[filename].size if filename in self.cacheMeta else 0
        )

        if spaceNeeded > 0:
            self._reduceCache(spaceNeeded)

        self.cacheMeta[filename] = CacheFileInfo(len(data), self._makeTimestamp())
        self._recalculateCacheSize()

        self._writeFile(self._getCacheFilePath(filename), data)

    def _readConfigFile(self) -> bytes | None:
        filepath = self._getConfigFilePath()
        print("Reading from config")

        return self._readFile(filepath)

    def _saveConfigFile(self, data: bytes) -> None:
        print("Writing to config")

        self._writeFile(self._getConfigFilePath(), data)

    def _reduceCache(self, overhead: int) -> None:
        newCacheSize = self._maxCacheSize() - overhead

        if self.state.cacheSize.value < newCacheSize:
            return

        print("Reducing cache to", newCacheSize)

        while self.state.cacheSize.value > newCacheSize:
            if len(self.cacheMeta) == 0:
                break

            self._deleteOldestCacheFile()

    def _deleteOldestCacheFile(self) -> None:
        oldestFile: str | None = None
        oldest = self._makeTimestamp() + 1

        for entry in self.cacheMeta.items():
            if entry[1].lastAccess < oldest:
                oldest = entry[1].lastAccess
                oldestFile = entry[0]

        if oldestFile is None:
            return

        self._removeCacheFile(self._getCacheFilePath(oldestFile))

    def _readFile(self, filepath: Path) -> bytes | None:
        if not filepath.exists():
            print("File doesn't exist", str(filepath.name))
            return None

        with open(filepath, "rb") as file:
            return file.read()

    def _writeFile(self, filepath: Path, data: bytes) -> None:
        if not self.allowSave:
            print("Saving not allowed")
            return

        with open(filepath, "wb") as file:
            file.write(data)
