from __future__ import annotations

from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.layers import UILayer


class IconToggleButton:
    def __init__(
        self,
        root: NodePath[PandaNode],
        icon: str,
        width: float,
        height: float,
        x: float = 0,
        y: float = 0,
        hAlign: HAlign = HAlign.CENTER,
        vAlign: VAlign = VAlign.CENTER,
        layer: UILayer = UILayer.CONTENT,
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

        self.button = DirectButton(
            parent=root,
            pos=(x + xPos, layer.value, y + yPos),
            scale=(width / 2, 1, height / 2),
            command=self.handleClick,
            image=icon,
            borderWidth=(0, 0),
            frameColor=(0, 0, 0, 0),
            rolloverSound=None,
            clickSound=None,
        )

        self.button.setBin("fixed", layer.value)

        self.button.setTransparency(TransparencyAttrib.MAlpha)

    def handleClick(self) -> None:
        print("click")

    def destroy(self) -> None:
        self.button.destroy()
