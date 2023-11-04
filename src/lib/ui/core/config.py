from direct.showbase.ShowBase import ShowBase

from lib.ui.core.anchors import UIAnchors
from lib.ui.core.font import UIFonts


class UIConfig:
    def __init__(self, base: ShowBase, scale: float = 1.0) -> None:
        self.anchors = UIAnchors(base, scale)
        self.fonts = UIFonts()

    def setScale(self, newScale: float) -> None:
        self.anchors.updateScale(newScale)

    def destroy(self) -> None:
        self.anchors.destroy()
