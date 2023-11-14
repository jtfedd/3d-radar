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
            config.anchors.top,
            config.fonts.bold,
            self.getClockStr(),
            y=-UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.BOTTOM,
        )

        self.updateTask = self.addTask(self.update, "update-clock", delay=1)

    def update(self, task: Task) -> int:
        self.text.updateText(self.getClockStr())

        return task.again

    def getClockStr(self) -> str:
        dateStr = "%A, %d %B %Y"
        timeStr = "%I:%M:%S %p"

        return datetime.datetime.now().strftime(dateStr + "\n" + timeStr)

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.text.destroy()
