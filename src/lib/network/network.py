from lib.app.state import AppState

from .location.provider import LocationProvider
from .nws.provider import NWSProvider
from .radar.provider import RadarProvider


class Network:
    def __init__(self, state: AppState) -> None:
        self.radar = RadarProvider()
        self.nws = NWSProvider()
        self.locations = LocationProvider(state)
