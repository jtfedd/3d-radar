import datetime

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight

from lib.app.files.manager import FileManager
from lib.data_connector.data_connector import DataConnector
from lib.data_provider.s3_data_provider import S3DataProvider
from lib.model.record import Record
from lib.model.scan import Scan


def getData() -> Scan:
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
    fileManager = FileManager()
    connector = DataConnector(provider, fileManager)

    return connector.load(record)


def defaultLight(base: ShowBase) -> None:
    dlight = DirectionalLight("dlight")
    dlight.setColor((1, 1, 1, 1))
    dlnp = base.render.attachNewNode(dlight)
    dlnp.setHpr(0, -60, 0)
    base.render.setLight(dlnp)

    alight = AmbientLight("alight")
    alight.setColor((0.2, 0.2, 0.2, 1))
    alnp = base.render.attachNewNode(alight)
    base.render.setLight(alnp)
