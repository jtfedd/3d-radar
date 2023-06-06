from direct.showbase.ShowBase import ShowBase

from lib.camera.camera_control import CameraControl
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.model.record import Record
from lib.geometry import marching_cubes
from lib.geometry import reshape
from lib.geometry import triangles_to_geometry

from panda3d.core import DirectionalLight, AmbientLight

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


class Viewer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setBackgroundColor(0, 0, 0, 1)
        self.cameraControl = CameraControl(self)

        # Make some light
        dlight = DirectionalLight("dlight")
        dlight.setColor((1, 1, 1, 1))
        dlnp = self.render.attachNewNode(dlight)
        dlnp.setHpr(0, -60, 0)
        self.render.setLight(dlnp)

        alight = AmbientLight("alight")
        alight.setColor((0.2, 0.2, 0.2, 1))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        self.radarBase = self.render.attachNewNode("radar")

        scan = getData()

        data = scan.reflectivity
        data = np.isnan(data)

        vertices, triangles = marching_cubes.getIsosurface(data, 0.5)
        vertices = reshape.reshape(vertices, scan)

        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        node = self.render.attachNewNode(geom)

        print("Done!")


app = Viewer()
app.run()
