import atexit

from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.render_volume.render_volume import VolumeRenderer
from lib.ui.ui import UI
from lib.util.util import defaultLight, getData

from .file_manager import FileManager
from .state import AppState


class App:
    def __init__(self, base: ShowBase) -> None:
        self.base = base
        self.base.setBackgroundColor(0, 0, 0, 1)

        self.fileManager = FileManager()

        self.state = AppState()
        self.loadConfig()

        self.ui = UI(self.base, self.state)

        self.cameraControl = CameraControl(self.base)
        defaultLight(self.base)

        self.volumeRenderer = VolumeRenderer(self.base, self.state)

        scan = getData()
        self.volumeRenderer.updateVolumeData(scan)

        atexit.register(self.saveConfig)

    def loadConfig(self) -> None:
        configPath = self.fileManager.getConfigFile()
        if not configPath.exists():
            return

        with configPath.open("r", encoding="utf-8") as f:
            jsonStr = f.read()
            self.state.fromJson(jsonStr)

    def saveConfig(self) -> None:
        with self.fileManager.getConfigFile().open("w", encoding="utf-8") as f:
            f.write(self.state.toJson())
