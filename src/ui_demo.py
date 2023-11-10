import random

from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from lib.ui.core.config import UIConfig
from lib.ui.ui import UI


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase

        self.uiConfig = UIConfig(base)
        self.ui = UI(self.uiConfig)

        self.accept("s", self.scale)

    def scale(self) -> None:
        self.uiConfig.setScale(random.randrange(5, 20) / 10.0)


base = ShowBase()

app = App(base)
base.run()
