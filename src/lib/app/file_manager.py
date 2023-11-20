from pathlib import Path

from platformdirs import user_cache_dir, user_config_dir


class FileManager:
    appName = "3dRadar"

    def __init__(self) -> None:
        self.configPath = Path(user_config_dir(self.appName, False, ensure_exists=True))
        self.cachePath = Path(user_cache_dir(self.appName, False, ensure_exists=True))
