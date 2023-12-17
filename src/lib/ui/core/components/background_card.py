from __future__ import annotations

import direct.gui.DirectGuiGlobals as DGG
from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath, PandaNode, TransparencyAttrib, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment

from .component import Component


class BackgroundCard(Component):
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
        x = correctXForAlignment(x, width, hAlign)
        y = correctYForAlignment(y, height, vAlign)

        self.card = DirectFrame(
            parent=root,
            frameSize=(
                -width / 2,
                width / 2,
                -height / 2,
                height / 2,
            ),
            frameColor=color,
            pos=(x, 1, y),
        )

        self.card.setTransparency(TransparencyAttrib.MAlpha)
        self.card.setBin("fixed", layer.value)
        self.card["state"] = DGG.NORMAL

    def updateColor(self, color: Vec4) -> None:
        self.card["frameColor"] = color

    def hide(self) -> None:
        self.card.hide()

    def show(self) -> None:
        self.card.show()

    def destroy(self) -> None:
        self.card.destroy()
