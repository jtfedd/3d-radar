import atexit
import sys

from direct.showbase.ShowBase import ShowBase

from lib.app.data_manager.manager import DataManager
from lib.map.map import Map
from lib.render_volume.render_volume import VolumeRenderer
from lib.ui.ui import UI

from .alerts.manager import AlertManager
from .context import AppContext
from .events import AppEvents
from .state import AppState


class App:
    def __init__(self, base: ShowBase) -> None:
        base.setBackgroundColor(0, 0, 0, 1)

        self.state = AppState()
        self.events = AppEvents()
        self.ctx = AppContext(base, self.events, self.state)

        self.ui = UI(self.ctx, self.state, self.events)
        self.map = Map(self.ctx, self.state, self.events)

        self.volumeRenderer = VolumeRenderer(self.ctx, self.state)
        self.alertManager = AlertManager(self.ctx, self.state, self.events)

        self.dataManager = DataManager(
            self.ctx,
            self.state,
            self.events,
        )

        self.events.clearDataAndExit.listen(lambda _: self.clearDataAndExit())

        atexit.register(self.destroy)

    def clearDataAndExit(self) -> None:
        self.ctx.fileManager.clearAllData()
        sys.exit()

    def destroy(self) -> None:
        self.dataManager.destroy()
        self.volumeRenderer.destroy()
        self.ui.destroy()

        self.ctx.fileManager.saveConfig()

        self.ctx.destroy()
        self.events.destroy()

        self.state.destroy()
