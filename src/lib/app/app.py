import atexit
import concurrent.futures

from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.map.map import Map
from lib.model.record import Record
from lib.render_volume.render_volume import VolumeRenderer
from lib.ui.ui import UI

from .alerts.manager import AlertManager
from .animation.manager import AnimationManager
from .context import AppContext
from .events import AppEvents
from .state import AppState


class App:
    def __init__(self, base: ShowBase) -> None:
        base.setBackgroundColor(0, 0, 0, 1)

        self.state = AppState()
        self.events = AppEvents()
        self.ctx = AppContext(base, self.events, self.state)

        self.loadConfig()

        self.ui = UI(self.ctx, self.state, self.events)

        self.cameraControl = CameraControl(self.ctx, self.events)
        self.volumeRenderer = VolumeRenderer(self.ctx, self.state)
        self.animationManager = AnimationManager(self.ctx, self.state, self.events)
        self.alertManager = AlertManager(self.ctx, self.state, self.events)

        self.map = Map(self.ctx, self.state, self.events)

        self.loadData()
        self.events.requestData.listen(lambda _: self.loadData())

        atexit.register(self.destroy)

    def loadData(self) -> None:
        radar = self.state.station.value

        records = self.ctx.services.radar.search(
            Record(
                radar,
                self.ctx.timeUtil.getQueryTime(),
            ),
            self.state.frames.value,
        )

        if len(records) == 0:
            raise ValueError("No Records Found")

        scans = {}

        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {
                executor.submit(self.ctx.services.radar.load, record)
                for record in records
            }
            for future in concurrent.futures.as_completed(futures):
                scan = future.result()
                scans[scan.record.key()] = scan

        self.ctx.radarCache.setData(scans)
        self.animationManager.setRecords(records)

    def loadConfig(self) -> None:
        raw = self.ctx.fileManager.readConfigFile()
        if raw is None:
            return

        jsonStr = raw.decode()
        if jsonStr == "":
            return

        self.state.fromJson(jsonStr)

    def saveConfig(self) -> None:
        self.ctx.fileManager.saveConfigFile(self.state.toJson().encode())

    def destroy(self) -> None:
        self.volumeRenderer.destroy()
        self.cameraControl.destroy()
        self.ui.destroy()
        self.ctx.destroy()
        self.events.destroy()

        self.saveConfig()
        self.state.destroy()
