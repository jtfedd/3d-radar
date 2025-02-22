import datetime

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.animation_frame import AnimationFrame
from lib.model.data_type import DataType
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class Label(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
        super().__init__()

        self.ctx = ctx
        self.state = state

        self.background = BackgroundCard(
            ctx.anchors.bottom,
            width=UIConstants.legendLabelWidth,
            height=UIConstants.legendLabelHeight,
            y=UIConstants.headerFooterHeight + UIConstants.legendPadding,
            vAlign=VAlign.BOTTOM,
            color=UIColors.LEGEND_BACKGROUND,
            layer=UILayer.LABEL_BACKGROUND,
        )

        self.product = Text(
            ctx.anchors.bottom,
            font=ctx.fonts.mono,
            text="",
            x=-(UIConstants.legendLabelWidth / 2) + UIConstants.legendPadding,
            y=UIConstants.headerFooterHeight
            + UIConstants.legendPadding
            + (UIConstants.legendLabelHeight / 2),
            vAlign=VAlign.BOTTOM,
            hAlign=HAlign.LEFT,
            layer=UILayer.LABEL_CONTENT,
        )

        self.unknown = Text(
            ctx.anchors.bottom,
            font=ctx.fonts.mono,
            text="No Data",
            y=UIConstants.headerFooterHeight
            + UIConstants.legendPadding
            + (UIConstants.legendLabelHeight / 2),
            vAlign=VAlign.CENTER,
            hAlign=HAlign.CENTER,
            layer=UILayer.LABEL_CONTENT,
        )

        self.time = Text(
            ctx.anchors.bottom,
            font=ctx.fonts.mono,
            text="",
            x=(UIConstants.legendLabelWidth / 2) - UIConstants.legendPadding,
            y=UIConstants.headerFooterHeight
            + UIConstants.legendPadding
            + (UIConstants.legendLabelHeight / 2),
            vAlign=VAlign.BOTTOM,
            hAlign=HAlign.RIGHT,
            layer=UILayer.LABEL_CONTENT,
        )

        self.triggerMany(
            [
                state.animationFrame,
                state.dataType,
                events.timeFormatChanged,
                state.station,
            ],
            self.updateLabel,
            triggerImmediately=True,
        )

    def updateLabel(self) -> None:
        frame: AnimationFrame | None = None
        frames = self.state.animationFrames.getValue()
        for f in frames:
            if f.id == self.state.animationFrame.value:
                frame = f

        if frame is None:
            self.product.hide()
            self.time.hide()
            self.unknown.show()
            return

        self.product.updateText(self.getProductText())
        self.time.updateText(self.getTimeText(frame))

        self.product.show()
        self.time.show()
        self.unknown.hide()

    def getProductText(self) -> str:
        radar = self.state.station.getValue()
        if self.state.dataType.value == DataType.REFLECTIVITY:
            product = "REFLECTIVITY"
        elif self.state.dataType.value == DataType.VELOCITY:
            product = "VELOCITY"
        else:
            return None

        return radar + "\n" + product

    def getTimeText(self, frame: AnimationFrame) -> str:
        return (
            self.formatTimestamp(frame.startTime)
            + "\n"
            + self.formatTimestamp(frame.endTime)
        )

    def formatTimestamp(self, timestamp: int) -> str:
        return self.ctx.timeUtil.formatTime(
            datetime.datetime.fromtimestamp(
                timestamp,
                datetime.timezone.utc,
            ),
            capitalizeMonth=True,
            seconds=True,
        )

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        self.product.destroy()
        self.time.destroy()
        self.unknown.destroy()
