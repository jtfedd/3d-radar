from direct.showbase.ShowBase import ShowBase
from panda3d.core import DynamicTextFont

from lib.ui.core.components.anchors import UIAnchors


class UIConfig:
    def __init__(self, base: ShowBase, scale: float = 1.0) -> None:
        self.font = DynamicTextFont("assets/font/Inter-Regular.ttf", 0)

        self.anchors = UIAnchors(base, scale)

    def setScale(self, newScale: float) -> None:
        self.anchors.updateScale(newScale)

    def destroy(self) -> None:
        self.anchors.destroy()
