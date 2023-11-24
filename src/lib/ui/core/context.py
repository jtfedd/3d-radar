from direct.showbase.ShowBase import ShowBase

from lib.app.state import AppState
from lib.ui.core.anchors import UIAnchors
from lib.ui.core.focus.focus_manager import FocusManager
from lib.ui.core.font import UIFonts
from lib.ui.core.keybindings.keybinding_manager import KeybindingManager
from lib.ui.events import UIEvents


class UIContext:
    def __init__(self, base: ShowBase, state: AppState, events: UIEvents) -> None:
        self.fonts = UIFonts()
        self.focusManager = FocusManager()
        self.keybindings = KeybindingManager(self.focusManager)
        self.anchors = UIAnchors(base, self.keybindings, state, events)

    def destroy(self) -> None:
        self.anchors.destroy()
        self.keybindings.destroy()
