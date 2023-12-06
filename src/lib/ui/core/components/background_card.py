from __future__ import annotations

from panda3d.core import NodePath, PandaNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.image import Image
from lib.ui.core.icons import Icons
from lib.ui.core.layers import UILayer


class BackgroundCard:
    def __init__(
        self,
        root: NodePath[PandaNode],
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        color: Vec4 = UIColors.BLACK,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.BACKGROUND,
    ) -> None:
        self.image = Image(
            root,
            Icons.BLANK,
            width=width,
            height=height,
            x=x,
            y=y,
            color=color,
            hAlign=hAlign,
            vAlign=vAlign,
            layer=layer,
        )

    def updateColor(self, color: Vec4) -> None:
        self.image.updateColor(color)

    def hide(self) -> None:
        self.image.hide()

    def show(self) -> None:
        self.image.show()

    def destroy(self) -> None:
        self.image.destroy()
