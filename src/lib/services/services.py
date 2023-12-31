from lib.app.files.manager import FileManager
from lib.network.network import Network

from .location.service import LocationService
from .nws.nws_service import NWSService
from .radar.radar_service import RadarService


class Services:
    def __init__(self, fileManager: FileManager, network: Network):
        self.nws = NWSService(fileManager, network)
        self.radar = RadarService(fileManager, network)
        self.locations = LocationService(network)
