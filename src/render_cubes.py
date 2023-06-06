from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.gradient.gradient import Gradient
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.model.record import Record
from lib.model.scan import Scan

import datetime

import random

import numpy as np


def getData():
    site = "KVWX"

    time = datetime.datetime(
        year=2019,
        month=6,
        day=26,
        hour=22,
        minute=11,
        second=5,
    )

    record = Record(site, time)

    provider = S3DataProvider()
    connector = DataConnector(provider)

    return connector.load(record)


class Viewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        self.cameraControl = CameraControl(self)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        print("Processing min and max")
        mask = np.isfinite(scan.reflectivity)
        min = np.min(scan.reflectivity[mask])
        max = np.max(scan.reflectivity[mask])

        self.gradient = Gradient(min, max)

        print("Building render volume")
        self.renderCubes(scan)

        print("Final scene post-processing")
        self.radarBase.clearModelNodes()
        self.radarBase.flattenStrong()

        print("Done!")

    def renderCubes(self, scan: Scan):
        azimuths = np.deg2rad(scan.azimuths)
        elevations = np.deg2rad(scan.elevations)

        sin_az = np.sin(azimuths)
        cos_az = np.cos(azimuths)

        sin_el = np.sin(elevations)
        cos_el = np.cos(elevations)

        for i in range(len(elevations)):
            for j in range(len(azimuths)):
                x_factor = cos_el[i] * sin_az[j]
                y_factor = cos_el[i] * cos_az[j]
                z_factor = sin_el[i]
                for k, rng in enumerate(scan.ranges):
                    if np.isnan(scan.reflectivity[i][j][k]):
                        continue

                    x = rng * x_factor
                    y = rng * y_factor
                    z = rng * z_factor

                    self.renderCube(x, y, z, scan.reflectivity[i][j][k])

    def renderCube(self, x, y, z, value):
        if random.randrange(0, 100) != 1:
            return

        cube = self.loader.loadModel("../assets/cube.glb")
        cube.reparentTo(self.radarBase)

        cube.setPos(x, y, z)
        cube.setColorScale(self.gradient.value(value))


app = Viewer()
app.run()
