from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class PanelHeader:
    def __init__(self, ctx: UIContext, text: str) -> None:
        self.root = ctx.anchors.topLeft.attachNewNode("panel-header")
        self.root.setZ(-UIConstants.headerFooterHeight)

        self.text = Text(
            root=self.root,
            font=ctx.fonts.bold,
            text=text,
            x=UIConstants.panelWidth / 2,
            y=-(UIConstants.panelHeaderHeight / 2),
            size=UIConstants.fontSizeHeader,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

        self.topBorder = BackgroundCard(
            root=self.root,
            width=UIConstants.panelWidth,
            height=UIConstants.panelBorderWidth,
            x=0,
            y=0,
            color=UIColors.BACKGROUND_LIGHT,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.BACKGROUND_DECORATION,
        )

    def hide(self) -> None:
        self.root.hide()

    def show(self) -> None:
        self.root.show()

    def destroy(self) -> None:
        self.text.destroy()
        self.topBorder.destroy()
        self.root.removeNode()
