from direct.showbase.DirectObject import DirectObject
from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.render_volume.render_volume import VolumeRenderer
from lib.util.util import defaultLight, getData


class App(DirectObject):
    def __init__(self, showbase: ShowBase) -> None:
        self.base = showbase
        self.base.setFrameRateMeter(True)
        self.base.setBackgroundColor(0, 0, 0, 1)

        self.cameraControl = CameraControl(self.base)
        defaultLight(self.base)

        self.volumeRenderer = VolumeRenderer(self.base)

        scan = getData()
        self.volumeRenderer.updateVolumeData(scan)


base = ShowBase()

maxBufferSize = base.win.get_gsg().get_max_buffer_texture_size()  # type: ignore
print("Max buffer size: " + str(maxBufferSize))

app = App(base)
base.run()
