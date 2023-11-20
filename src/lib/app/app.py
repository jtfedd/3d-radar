import atexit

from direct.showbase.ShowBase import ShowBase

from lib.app.app_config import AppConfig
from lib.app.file_manager import FileManager
from lib.ui.core.config import UIConfig
from lib.ui.ui import UI


class App:
    def __init__(self, base: ShowBase) -> None:
        self.base = base

        self.fileManager = FileManager()

        self.config = AppConfig()
        self.loadConfig()

        self.uiConfig = UIConfig(self.base)
        self.ui = UI(self.uiConfig)

        atexit.register(self.saveConfig)

    def loadConfig(self) -> None:
        configPath = self.fileManager.getConfigFile()
        if not configPath.exists():
            return

        with configPath.open("r", encoding="utf-8") as f:
            jsonStr = f.read()
            self.config.fromJson(jsonStr)

    def saveConfig(self) -> None:
        with self.fileManager.getConfigFile().open("w", encoding="utf-8") as f:
            f.write(self.config.toJson())
