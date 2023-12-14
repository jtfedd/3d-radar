import atexit
import concurrent.futures
import datetime

from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.model.record import Record
from lib.render_volume.render_volume import VolumeRenderer
from lib.ui.ui import UI
from lib.util.util import defaultLight

from .animation.manager import AnimationManager
from .context import AppContext
from .events import AppEvents
from .state import AppState


class App:
    def __init__(self, base: ShowBase) -> None:
        base.setBackgroundColor(0, 0, 0, 1)
        defaultLight(base)

        self.state = AppState()
        self.events = AppEvents()
        self.ctx = AppContext(base, self.events, self.state)

        self.loadConfig()

        self.ui = UI(self.ctx, self.state, self.events)

        self.cameraControl = CameraControl(self.ctx, self.events)
        self.volumeRenderer = VolumeRenderer(self.ctx, self.state, self.events)
        self.animationManager = AnimationManager(self.ctx, self.state, self.events)

        self.loadData()
        self.events.requestData.listen(lambda _: self.loadData())

        atexit.register(self.destroy)

    def loadData(self) -> None:
        radar = self.state.station.value
        year = self.state.year.value
        month = self.state.month.value
        day = self.state.day.value
        time = self.state.time.value

        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])

        records = self.ctx.network.search(
            Record(
                radar,
                datetime.datetime(
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=59,
                    tzinfo=datetime.timezone.utc,
                ),
            ),
            self.state.frames.value,
        )

        if len(records) == 0:
            raise ValueError("No Records Found")

        scans = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.ctx.network.load, record) for record in records
            }
            for future in concurrent.futures.as_completed(futures):
                scan = future.result()
                scans[scan.record.key()] = scan

        self.volumeRenderer.setData(scans)
        self.animationManager.setRecords(records)

    def loadConfig(self) -> None:
        configPath = self.ctx.fileManager.getConfigFile()
        if not configPath.exists():
            return

        with configPath.open("r", encoding="utf-8") as f:
            jsonStr = f.read()
            if jsonStr == "":
                return
            self.state.fromJson(jsonStr)

    def saveConfig(self) -> None:
        with self.ctx.fileManager.getConfigFile().open("w", encoding="utf-8") as f:
            f.write(self.state.toJson())

    def destroy(self) -> None:
        self.volumeRenderer.destroy()
        self.cameraControl.destroy()
        self.ui.destroy()
        self.ctx.destroy()
        self.events.destroy()

        self.saveConfig()
        self.state.destroy()
