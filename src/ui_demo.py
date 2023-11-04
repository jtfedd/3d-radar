from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from lib.ui.core.config import UIConfig
from lib.ui.ui import UI


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        self.uiConfig = UIConfig(base)
        self.ui = UI(self.uiConfig)


base = ShowBase()

app = App(base)
base.run()
