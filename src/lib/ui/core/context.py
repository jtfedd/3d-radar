from direct.showbase.ShowBase import ShowBase

from lib.ui.core.anchors import UIAnchors
from lib.ui.core.focus.focus_manager import FocusManager
from lib.ui.core.font import UIFonts
from lib.ui.core.keybindings.keybinding_manager import KeybindingManager


class UIContext:
    def __init__(self, base: ShowBase, scale: float = 1.0) -> None:
        self.focusManager = FocusManager()
        self.keybindings = KeybindingManager(self.focusManager)
        self.anchors = UIAnchors(base, self.keybindings, scale)
        self.fonts = UIFonts()

    def setScale(self, newScale: float) -> None:
        self.anchors.updateScale(newScale)

    def destroy(self) -> None:
        self.anchors.destroy()
