from __future__ import annotations

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import NodePath, PandaNode, Vec4

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.layers import UILayer


class BackgroundCard:
    def __init__(
        self,
        root: NodePath[PandaNode],
        x: float,
        y: float,
        width: float,
        height: float,
        color: Vec4,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.BACKGROUND,
    ) -> None:
        xPos = 0.0
        if hAlign == HAlign.LEFT:
            xPos = width / 2
        elif hAlign == HAlign.RIGHT:
            xPos = -width / 2

        yPos = 0.0
        if vAlign == VAlign.TOP:
            yPos = -height / 2
        elif vAlign in (VAlign.BOTTOM, VAlign.BASELINE):
            yPos = height / 2

        self.card = OnscreenImage(
            image="assets/white.png",
            pos=(x + xPos, 0, y + yPos),
            scale=(width / 2, 1, height / 2),
            parent=root,
            color=color,
            sort=layer.value,
        )

    def destroy(self) -> None:
        self.card.destroy()
