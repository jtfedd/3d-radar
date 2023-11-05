from __future__ import annotations

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, PandaNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment


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
        x = correctXForAlignment(x, width, hAlign)
        y = correctYForAlignment(y, height, vAlign)

        self.card = OnscreenImage(
            image="assets/white.png",
            pos=(x, 0, y),
            scale=(width / 2, 1, height / 2),
            parent=root,
            color=color,
        )

        self.card.setBin("fixed", layer.value)

    def destroy(self) -> None:
        self.card.destroy()
