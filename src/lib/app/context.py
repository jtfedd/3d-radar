from direct.showbase.ShowBase import ShowBase

from lib.network.network import Network
from lib.network.radar.s3_data_provider import S3DataProvider

from .animation.manager import AnimationManager
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
        self.inputManager = InputManager(self.focusManager, state, events.input)
        self.windowManager = WindowManager(events.window)
        self.network = Network(S3DataProvider(), self.fileManager)
        self.animationManager = AnimationManager(events)

    def destroy(self) -> None:
        self.inputManager.destroy()
        self.windowManager.destroy()
        self.animationManager.destroy()
