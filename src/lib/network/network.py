from .nws.api import NWSApi
from .radar.provider import RadarProvider


class Network:
    def __init__(self) -> None:
        self.radar = RadarProvider()
        self.nws = NWSApi()
