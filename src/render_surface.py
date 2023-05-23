from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.data_connector.request import Request
from lib.geometry import marching_cubes

from panda3d.core import DirectionalLight, AmbientLight

import mcubes


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

        # Make some light
        dlight = DirectionalLight("dlight")
        dlight.setColor((0.8, 0.8, 0.5, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        alight = AmbientLight("alight")
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        scan.printInfo()

        # data = scan.reflectivityMatrix()
        # print(data.shape)
        # print(data)

        # vertices, triangles = marching_cubes.getIsosurface(data, 0)
        # mcubes.export_obj(vertices, triangles, "../test.obj")

        # sharp_geom = marching_cubes.getGeometry(data, 0, smooth=False)
        # sharp_node = self.render.attachNewNode(sharp_geom)

        print("Done!")


app = Viewer()
app.run()
