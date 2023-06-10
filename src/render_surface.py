"""Example script to render isosurface from scan data"""

import datetime

import numpy as np
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight

from lib.camera.camera_control import CameraControl
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.geometry import marching_cubes, reshape, triangles_to_geometry
from lib.model.record import Record
from lib.model.scan import Scan


def getData() -> Scan:
    """Returns some default data for the sample app"""
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
    """Example app"""

    def __init__(self) -> None:
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

        scan = getData()

        data = scan.reflectivity
        data = np.isnan(data)

        vertices, triangles = marching_cubes.getIsosurface(data, 0.5)
        vertices = reshape.reshape(vertices, scan)

        geom = triangles_to_geometry.getGeometry(vertices, triangles, smooth=False)
        self.render.attachNewNode(geom)

        print("Done!")


app = Viewer()
app.run()
