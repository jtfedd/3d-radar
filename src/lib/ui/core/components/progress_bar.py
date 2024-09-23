from __future__ import annotations

from panda3d.core import NodePath, PandaNode

from lib.ui.core.alignment import HAlign, VAlign
from lib.ui.core.colors import UIColors
from lib.ui.core.components.background_card import BackgroundCard
from lib.ui.core.constants import UIConstants
from lib.ui.core.layers import UILayer
from lib.ui.core.util import correctXForAlignment

from .component import Component


class ProgressBar(Component):
    def __init__(
        self,
        root: NodePath[PandaNode],
        x: float,
        y: float,
        width: float,
        hAlign: HAlign,
        progress: float,
        layer: UILayer = UILayer.CONTENT_INTERACTION,
        bgLayer: UILayer = UILayer.CONTENT,
    ) -> None:
        self.width = width

        xPos = correctXForAlignment(x, width, hAlign)
        xPos -= width / 2

        self.bg = BackgroundCard(
            root=root,
            width=width,
            height=UIConstants.progressHeight,
            x=xPos,
            y=y,
            color=UIColors.PROGRESS_BG,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=bgLayer,
        )

        self.progressBar = BackgroundCard(
            root=root,
            width=0,
            height=UIConstants.progressHeight,
            x=xPos,
            y=y,
            color=UIColors.PROGRESS_BAR,
            hAlign=HAlign.LEFT,
            vAlign=VAlign.CENTER,
            layer=layer,
        )

        self.setProgress(progress)

    def setProgress(self, value: float) -> None:
        self.progressBar.updateSize(self.width * value, UIConstants.progressHeight)

    def destroy(self) -> None:
        self.bg.destroy()
        self.progressBar.destroy()
