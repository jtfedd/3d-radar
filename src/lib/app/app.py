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
        self.config.fromJson(self.fileManager.loadConfig())

        self.uiConfig = UIConfig(self.base)
        self.ui = UI(self.uiConfig)

        atexit.register(self.saveConfig)

    def saveConfig(self) -> None:
        self.fileManager.saveConfig(self.config.toJson())
