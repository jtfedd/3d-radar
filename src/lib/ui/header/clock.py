import datetime

from direct.task.Task import Task

from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class Clock:
    def __init__(self, ctx: UIContext):
        self.text = Text(
            ctx.anchors.topRight,
            ctx.fonts.medium,
            self.getClockStr(),
            x=-UIConstants.clockPadding,
            y=-UIConstants.headerFooterHeight / 2,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.BOTTOM,
        )

        self.background = BackgroundCard(
            ctx.anchors.topRight,
            width=UIConstants.clockWidth,
            height=UIConstants.headerFooterHeight,
            color=UIColors.INSET,
            vAlign=VAlign.TOP,
            hAlign=HAlign.RIGHT,
            layer=UILayer.BACKGROUND_DECORATION,
        )

        self.updateTask = ctx.appContext.base.addTask(
            self.update, "update-clock", delay=1
        )

    def update(self, task: Task) -> int:
        self.text.updateText(self.getClockStr())

        return task.again

    def getClockStr(self) -> str:
        dateStr = "%d %b %Y"
        timeStr = "%I:%M %p"

        return datetime.datetime.now().strftime(dateStr + "\n" + timeStr)

    def destroy(self) -> None:
        self.updateTask.cancel()
        self.text.destroy()
        self.background.destroy()
