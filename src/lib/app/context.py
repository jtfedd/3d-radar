from direct.showbase.ShowBase import ShowBase

from lib.app.animation.manager import AnimationManager
from lib.network.network import Network
from lib.services.services import Services

from .events import AppEvents
from .files.manager import FileManager
from .focus.manager import FocusManager
from .input.manager import InputManager
from .state import AppState
from .task.manager import TaskManager
from .time.util import TimeUtil
from .window.manager import WindowManager


class AppContext:
    def __init__(self, base: ShowBase, events: AppEvents, state: AppState) -> None:
        self.base = base
        self.fileManager = FileManager(state, events)
        self.taskManager = TaskManager(base)
        self.focusManager = FocusManager()
        self.inputManager = InputManager(self.focusManager, state, events.input)
        self.windowManager = WindowManager(base, events.window)
        self.animationManager = AnimationManager(base, state, events)
        self.services = Services(self.fileManager, Network())
        self.timeUtil = TimeUtil(state, events, self.services)

    def destroy(self) -> None:
        self.animationManager.destroy()
        self.inputManager.destroy()
        self.windowManager.destroy()
        self.services.destroy()
        self.taskManager.destroy()
        self.fileManager.destroy()
