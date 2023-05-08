from direct.showbase.ShowBase import ShowBase

from src.camera.camera_control import CameraControl
from src.gradient import Gradient
from src.data_connector.data_connector import DataConnector
from src.data_provider.s3_data_provider import S3DataProvider
from src.data_connector.request import Request

import datetime

import random


site = "KVWX"
date = datetime.date(year=2019, month=6, day=26)
time = datetime.time(hour=22, minute=11, second=5)

request = Request(site, date, time)

provider = S3DataProvider()
connector = DataConnector(provider)

scan = connector.load(request)
points = scan.points()

with open(request.cacheKey() + ".xyz", "w") as f:
    for p in points:
        f.write("{0} {1} {2}\n".format(p.x, p.y, p.z))
