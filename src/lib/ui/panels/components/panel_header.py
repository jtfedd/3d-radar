from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.components.text import Text
from lib.ui.core.config import UIConfig
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer


class PanelHeader:
    def __init__(self, config: UIConfig, text: str) -> None:
        self.text = Text(
            root=config.anchors.topLeft,
            font=config.fonts.bold,
            text=text,
            x=UIConstants.panelWidth / 2,
            y=-UIConstants.headerFooterHeight - (UIConstants.panelHeaderHeight / 2),
            size=UIConstants.fontSizeTitle,
            hAlign=HAlign.CENTER,
            vAlign=VAlign.CENTER,
        )

        self.topBorder = BackgroundCard(
            root=config.anchors.topLeft,
            width=UIConstants.panelWidth,
            height=UIConstants.panelBorderWidth,
            x=0,
            y=-UIConstants.headerFooterHeight,
            color=UIColors.WHITE,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.TOP,
            layer=UILayer.BACKGROUND_DECORATION,
        )

    def destroy(self) -> None:
        self.text.destroy()
        self.topBorder.destroy()
