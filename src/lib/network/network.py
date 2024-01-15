from .location.provider import LocationProvider
from .nws.provider import NWSProvider
from .radar.provider import RadarProvider


class Network:
    def __init__(self) -> None:
        self.radar = RadarProvider()
        self.nws = NWSProvider()
        self.locations = LocationProvider()
