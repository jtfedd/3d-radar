from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.gradient.gradient import Gradient
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.data_connector.request import Request

import datetime

import random


def getData():
    site = "KVWX"
    date = datetime.date(year=2019, month=6, day=26)
    time = datetime.time(hour=22, minute=11, second=5)

    request = Request(site, date, time)

    provider = S3DataProvider()
    connector = DataConnector(provider)

    return connector.load(request)


class Viewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        self.cameraControl = CameraControl(self)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        print("Processing min and max")
        self.minVal = 1000000000
        self.maxVal = -1000000000
        scan.foreach(lambda p: self.processMinMax(p))
        self.gradient = Gradient(self.minVal, self.maxVal)

        print("Building render volume")
        scan.foreach(lambda p: self.renderCube(p))

        print("Final scene post-processing")
        self.radarBase.clearModelNodes()
        self.radarBase.flattenStrong()

        print("Done!")

    def processMinMax(self, point):
        if point.value < self.minVal:
            self.minVal = point.value
        if point.value > self.maxVal:
            self.maxVal = point.value

    def renderCube(self, point):
        if random.randrange(0, 100) != 1:
            return

        cube = self.loader.loadModel("../assets/cube.glb")
        cube.reparentTo(self.radarBase)

        cube.setPos(point.x, point.y, point.z)
        cube.setColorScale(self.gradient.value(point.value))


app = Viewer()
app.run()
