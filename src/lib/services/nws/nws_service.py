from typing import Dict

from lib.app.files.manager import FileManager
from lib.model.radar_station import RadarStation
from lib.network.network import Network


class NWSService:
    def __init__(self, fileManager: FileManager, network: Network) -> None:
        self.network = network
        self.fileManager = fileManager

        self.radarStations = self.preloadStations()

    def getStation(self, code: str) -> RadarStation | None:
        if code not in self.radarStations:
            return None

        return self.radarStations[code]

    def preloadStations(self) -> Dict[str, RadarStation]:
        stations = self.network.nws.getRadarStations()
        if stations:
            return stations

        # TODO fall back to cached stations if it couldn't be loaded

        raise RuntimeError("Could not load stations")
