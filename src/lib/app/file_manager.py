from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir


class FileManager:
    appName = "3dRadar"

    def __init__(self) -> None:
        self.configPath = Path(user_config_dir(self.appName, False, ensure_exists=True))
        self.cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))

    def getConfigFile(self) -> Path:
        return self.configPath.joinpath("config.json")

    def loadConfig(self) -> str:
        configPath = self.getConfigFile()
        if not configPath.exists():
            return "{}"

        with self.configPath.joinpath("config.json").open("r", encoding="utf-8") as f:
            return f.read()

    def saveConfig(self, configStr: str) -> None:
        with self.configPath.joinpath("config.json").open("w", encoding="utf-8") as f:
            f.write(configStr)
