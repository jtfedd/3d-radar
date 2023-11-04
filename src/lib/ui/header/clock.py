import datetime

from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants


class Clock(DirectObject):
    def __init__(self, config: UIConfig):
        self.config = config

        self.text = Text(
            config.anchors.topCenter,
            config.fonts.bold,
            self.getClockStr(),
            y=-UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

        self.updateTask = self.addTask(self.update, "update-clock")

    def update(self, task: Task) -> int:
        self.text.updateText(self.getClockStr())

        return task.cont

    def getClockStr(self) -> str:
        return datetime.datetime.now().strftime("%a %d %b %Y, %I:%M:%S %p")

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.text.destroy()
