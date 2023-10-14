from direct.gui.DirectGui import DirectSlider
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

        self.minSlider = DirectSlider(
            pos=(0, 0, -0.7),
            scale=0.6,
            range=(0, 1),
            value=0,
            pageSize=0.1,
            command=self.updateMin,
        )

        self.maxSlider = DirectSlider(
            pos=(0, 0, -0.8),
            scale=0.6,
            range=(0, 10),
            value=1,
            pageSize=0.1,
            command=self.updateMax,
        )

        self.slider = DirectSlider(
            pos=(0, 0, -0.9),
            scale=0.6,
            range=(-0.5, 1.0),
            value=0.5,
            pageSize=0.05,
            command=self.updateDensityExponent,
        )

    def updateDensityExponent(self) -> None:
        self.volumeRenderer.updateDensityExponent(float(self.slider["value"]))

    def updateMin(self) -> None:
        self.volumeRenderer.updateMin(float(self.minSlider["value"]))

    def updateMax(self) -> None:
        self.volumeRenderer.updateMax(float(self.maxSlider["value"]))


base = ShowBase()

maxBufferSize = base.win.get_gsg().get_max_buffer_texture_size()  # type: ignore
print("Max buffer size: " + str(maxBufferSize))

app = App(base)
base.run()
