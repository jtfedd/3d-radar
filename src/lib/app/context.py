from direct.showbase.ShowBase import ShowBase

from .events import AppEvents
from .files.manager import FileManager
from .focus.manager import FocusManager
from .input.manager import InputManager
from .state import AppState
from .window.manager import WindowManager


class AppContext:
    def __init__(self, base: ShowBase, events: AppEvents, state: AppState) -> None:
        self.base = base
        self.fileManager = FileManager()
        self.focusManager = FocusManager()
        self.keybindings = InputManager(self.focusManager, state, events.input)
        self.windowManager = WindowManager(events.window)

    def destroy(self) -> None:
        self.keybindings.destroy()
        self.windowManager.destroy()
