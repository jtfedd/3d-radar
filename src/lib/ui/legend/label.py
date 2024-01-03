from lib.app.state import AppState
from lib.model.data_type import DataType
from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.util.events.listener import Listener


class Label(Listener):
    def __init__(self, ctx: UIContext, state: AppState):
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
            vAlign=VAlign.CENTER,
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
            vAlign=VAlign.CENTER,
            hAlign=HAlign.RIGHT,
            layer=UILayer.LABEL_CONTENT,
        )

        self.updateLabel()
        self.listen(state.animationFrame, lambda _: self.updateLabel())
        self.listen(state.dataType, lambda _: self.updateLabel())

    def updateLabel(self) -> None:
        productText = self.getProductText()
        timeText = self.getTimeText()

        if not productText or not timeText:
            self.product.hide()
            self.time.hide()
            self.unknown.show()
            return

        self.product.show()
        self.time.show()
        self.unknown.hide()

        self.product.updateText(productText)
        self.time.updateText(timeText)

    def getProductText(self) -> str | None:
        if not self.state.animationFrame.value:
            return None

        scan = self.ctx.appContext.radarCache.get(self.state.animationFrame.value)
        if not scan:
            return None

        radar = scan.record.station
        if self.state.dataType.value == DataType.REFLECTIVITY:
            product = "REFLECTIVITY"
        elif self.state.dataType.value == DataType.VELOCITY:
            product = "VELOCITY"
        else:
            return None

        return radar + " " + product

    def getTimeText(self) -> str | None:
        if not self.state.animationFrame.value:
            return None

        scan = self.ctx.appContext.radarCache.get(self.state.animationFrame.value)
        if not scan:
            return None

        return self.ctx.appContext.timeUtil.formatTime(
            scan.record.time,
            capitalizeMonth=True,
        )

    def destroy(self) -> None:
        super().destroy()

        self.background.destroy()
        self.product.destroy()
        self.time.destroy()
        self.unknown.destroy()
