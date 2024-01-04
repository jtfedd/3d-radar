import datetime

from direct.task.Task import Task

from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class Clock(Listener):
    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__()

        self.ctx = ctx

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

        self.listen(
            events.timeFormatChanged,
            lambda _: self.text.updateText(self.getClockStr()),
        )

    def update(self, task: Task) -> int:
        self.text.updateText(self.getClockStr())

        return task.again

    def getClockStr(self) -> str:
        return self.ctx.appContext.timeUtil.formatTime(
            datetime.datetime.now(),
            sep="\n",
        )

    def destroy(self) -> None:
        super().destroy()

        self.updateTask.cancel()
        self.text.destroy()
        self.background.destroy()
