from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir


class FileManager:
    appName = "3dRadar"

    def __init__(self) -> None:
        self.configPath = Path(user_config_dir(self.appName, False, ensure_exists=True))
        self.cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))

    def getConfigFile(self) -> Path:
        return self.configPath.joinpath("config.json")

    def getCacheFile(self, filename: str) -> Path:
        return self.cachePath.joinpath(filename)

    def removeCacheFile(self, filename: str) -> None:
        file = self.getCacheFile(filename)
        if not file.exists():
            return

        file.unlink()

    def clearCache(self) -> None:
        for file in self.cachePath.iterdir():
            file.unlink()
