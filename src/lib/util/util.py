import datetime

from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight

from lib.model.record import Record
from lib.model.scan import Scan
from lib.network.network import Network


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

    connector = Network()

    return connector.radar.load(record)


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


def nextPowerOf2(n: int) -> int:
    return 2 ** (n - 1).bit_length()  # type: ignore
