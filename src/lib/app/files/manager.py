from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir


class FileManager:
    appName = "Stormfront"

    def __init__(self) -> None:
        self.configPath = Path(user_config_dir(self.appName, False, ensure_exists=True))
        self.cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))

    def getConfigFile(self) -> Path:
        return self.configPath.joinpath("config.json")

    def getCacheFile(self, filename: str) -> Path:
        return self.cachePath.joinpath(filename)

    def clearCache(self) -> None:
        for file in self.cachePath.iterdir():
            self.removeCacheFile(file)

    def removeCacheFile(self, file: Path) -> None:
        if not file.exists():
            return

        print("Removing", str(file))
        file.unlink()
