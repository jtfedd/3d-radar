from __future__ import annotations

from direct.gui.DirectButton import DirectButton
from panda3d.core import NodePath, PandaNode, TransparencyAttrib

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment, correctYForAlignment


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
        x = correctXForAlignment(x, width, hAlign)
        y = correctYForAlignment(y, height, vAlign)

        self.button = DirectButton(
            parent=root,
            image=icon,
            command=self.handleClick,
            pos=(x, 0, y),
            scale=(width / 2, 1, height / 2),
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
