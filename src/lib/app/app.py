from direct.showbase.ShowBase import ShowBase

from lib.app.file_manager import FileManager
from lib.ui.core.config import UIConfig
from lib.ui.ui import UI


class App(ShowBase):
    def __init__(self) -> None:
        super().__init__()

        self.fileManager = FileManager()

        self.uiConfig = UIConfig(self)
        self.ui = UI(self.uiConfig)
