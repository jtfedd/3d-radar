import direct.showbase.ShowBase

from lib.camera.camera_control import CameraControl
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.model.record import Record
from lib.geometry import marching_cubes
from lib.geometry import reshape
from lib.geometry import triangles_to_geometry

from panda3d.core import DirectionalLight, AmbientLight, TransparencyAttrib

import numpy as np
import datetime


def getData():
    site = "KVWX"
    time = datetime.datetime(
        2019,
        6,
        26,
        hour=22,
        minute=11,
        second=5,
        tzinfo=datetime.timezone.utc,
    )

    record = Record(site, time)

    provider = S3DataProvider()
    connector = DataConnector(provider)

    return connector.load(record)


class Viewer(direct.showbase.ShowBase.ShowBase):
    def __init__(self):
        direct.showbase.ShowBase.ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        self.cameraControl = CameraControl(self)
        self.accept("w", self.toggle_wireframe)

        # Make some light
        dlight = DirectionalLight("dlight")
        dlight.setColor((1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        alight = AmbientLight("alight")
        alight.setColor((0.7, 0.7, 0.7, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        data = scan.reflectivity

        booleanData = np.isnan(data)
        vertices, triangles = marching_cubes.getIsosurface(booleanData, 0.5)
        vertices = reshape.reshape(vertices, scan)
        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        node = self.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(1, 1, 1, 0.1)

        minValue = np.nanmin(data)
        data = np.nan_to_num(data, nan=minValue)
        data = np.negative(data)

        self.addIso(data, scan, 5, 0, 0, 1, 0.2)
        self.addIso(data, scan, -10, 0, 1, 0, 0.3)
        self.addIso(data, scan, -35, 1, 1, 0, 0.4)
        self.addIso(data, scan, -60, 1, 0, 0, 0.5)

        print("Done!")

    def addIso(self, data, scan, level, r, g, b, a):
        print("Iso", level)

        vertices, triangles = marching_cubes.getIsosurface(data, level)
        vertices = reshape.reshape(vertices, scan)
        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)

        node = self.render.attachNewNode(geom)
        node.setTransparency(TransparencyAttrib.MAlpha)
        node.setColorScale(r, g, b, a)


app = Viewer()
app.run()
