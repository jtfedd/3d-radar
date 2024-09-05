from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir


class FileManager:
    appName = "Stormfront"

    def __init__(self) -> None:
        self._configPath = Path(
            user_config_dir(self.appName, False, ensure_exists=True)
        )
        self._cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))

        print("Config", self._configPath.absolute())
        print("Cache", self._cachePath.absolute())

        self._initializeCacheMeta()

    def _getConfigFilePath(self) -> Path:
        return self._configPath.joinpath("config.json")

    def _getCacheFilePath(self, filename: str) -> Path:
        return self._cachePath.joinpath(filename)

    def _initializeCacheMeta(self) -> None:
        for p in self._cachePath.iterdir():
            print(p.name)
            print(p.stat().st_size)

    def _clearCache(self) -> None:
        for file in self._cachePath.iterdir():
            self._removeCacheFile(file)

    def _removeCacheFile(self, file: Path) -> None:
        if not file.exists():
            return

        print("Removing", str(file))
        file.unlink()

    def readCacheFile(self, filename: str) -> bytes | None:
        filepath = self._getCacheFilePath(filename)
        print("Reading from cache", filename)

        return self._readFile(filepath)

    def saveCacheFile(self, filename: str, data: bytes) -> None:
        print("Writing to cache", filename)

        self._writeFile(self._getCacheFilePath(filename), data)

    def readConfigFile(self) -> bytes | None:
        filepath = self._getConfigFilePath()
        print("Reading from config")

        return self._readFile(filepath)

    def saveConfigFile(self, data: bytes) -> None:
        print("Writing to config")

        self._writeFile(self._getConfigFilePath(), data)

    def _readFile(self, filepath: Path) -> bytes | None:
        if not filepath.exists():
            return None

        with open(filepath, "rb") as file:
            return file.read()

    def _writeFile(self, filepath: Path, data: bytes) -> None:
        with open(filepath, "wb") as file:
            file.write(data)
