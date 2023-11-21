from lib.ui.core.focus.focus_manager import FocusManager
from lib.util.uuid import uuid


class Focusable:
    def __init__(self, focusManager: FocusManager):
        self.focusManager = focusManager
        self.focusID = uuid()

    def onFocus(self, focused: bool) -> None:
        self.focusManager.focus(self.focusID, focused)

    def destroy(self) -> None:
        self.focusManager.focus(self.focusID, False)
