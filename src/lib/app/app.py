import atexit

from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.model.record import Record
from lib.render_volume.render_volume import VolumeRenderer
from lib.ui.ui import UI
from lib.util.util import defaultLight, getData

from .context import AppContext
from .events import AppEvents
from .state import AppState


class App:
    def __init__(self, base: ShowBase) -> None:
        base.setBackgroundColor(0, 0, 0, 1)
        defaultLight(base)

        self.events = AppEvents()
        self.state = AppState()
        self.ctx = AppContext(base, self.events, self.state)

        self.loadConfig()

        self.ui = UI(self.ctx, self.state, self.events)

        self.cameraControl = CameraControl(self.ctx, self.events)
        self.volumeRenderer = VolumeRenderer(self.ctx, self.state, self.events)

        scan = getData()
        self.volumeRenderer.updateVolumeData(scan)

        self.events.ui.panels.requestData.listen(self.loadData)

        atexit.register(self.saveConfig)

    def loadData(self, record: Record) -> None:
        scan = self.ctx.network.load(record)
        self.volumeRenderer.updateVolumeData(scan)

    def loadConfig(self) -> None:
        configPath = self.ctx.fileManager.getConfigFile()
        if not configPath.exists():
            return

        with configPath.open("r", encoding="utf-8") as f:
            jsonStr = f.read()
            self.state.fromJson(jsonStr)

    def saveConfig(self) -> None:
        with self.ctx.fileManager.getConfigFile().open("w", encoding="utf-8") as f:
            f.write(self.state.toJson())
