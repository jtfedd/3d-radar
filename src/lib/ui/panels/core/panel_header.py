from lib.ui.context import UIContext
from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.button import Button
from lib.ui.core.components.text import Text
from lib.ui.core.constants import UIConstants
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer
from lib.ui.panels.events import PanelEvents
from lib.ui.panels.panel_type import PanelType
from lib.util.events.listener import Listener


class PanelHeader(Listener):
    def __init__(self, ctx: UIContext, events: PanelEvents, text: str) -> None:
        super().__init__()

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

        closeButtonSize = UIConstants.panelHeaderHeight - UIConstants.panelBorderWidth

        self.closeButton = Button(
            root=self.root,
            ctx=ctx,
            width=closeButtonSize,
            height=closeButtonSize,
            x=UIConstants.panelWidth,
            y=-UIConstants.panelBorderWidth,
            hAlign=HAlign.RIGHT,
            vAlign=VAlign.TOP,
            icon=Icons.X,
            iconWidth=closeButtonSize,
            iconHeight=closeButtonSize,
        )

        self.listen(
            self.closeButton.onClick, lambda _: events.panelChanged.send(PanelType.NONE)
        )

    def hide(self) -> None:
        self.root.hide()

    def show(self) -> None:
        self.root.show()

    def destroy(self) -> None:
        super().destroy()

        self.text.destroy()
        self.topBorder.destroy()
        self.closeButton.destroy()
        self.root.removeNode()
