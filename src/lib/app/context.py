from direct.showbase.ShowBase import ShowBase

from lib.network.network import Network
from lib.services.services import Services

from .cache.radar_cache import RadarCache
from .events import AppEvents
from .files.manager import FileManager
from .focus.manager import FocusManager
from .input.manager import InputManager
from .state import AppState
from .time.util import TimeUtil
from .window.manager import WindowManager


class AppContext:
    def __init__(self, base: ShowBase, events: AppEvents, state: AppState) -> None:
        self.base = base
        self.fileManager = FileManager()
        self.focusManager = FocusManager()
        self.inputManager = InputManager(self.focusManager, state, events.input)
        self.windowManager = WindowManager(base, events.window)
        self.services = Services(self.fileManager, Network())
        self.radarCache = RadarCache()
        self.timeUtil = TimeUtil(state, events, self.services)

    def destroy(self) -> None:
        self.inputManager.destroy()
        self.windowManager.destroy()

        self.services.destroy()
