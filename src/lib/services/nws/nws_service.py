from typing import Dict, List

from lib.app.files.manager import FileManager
from lib.model.alert import Alert
from lib.model.alert_type import AlertType
from lib.model.radar_station import RadarStation
from lib.network.network import Network


class NWSService:
    def __init__(self, fileManager: FileManager, network: Network) -> None:
        self.network = network
        self.fileManager = fileManager

        self.radarStations = self.preloadStations()

    def getStation(self, stationID: str) -> RadarStation | None:
        if stationID not in self.radarStations:
            return None

        return self.radarStations[stationID]

    def preloadStations(self) -> Dict[str, RadarStation]:
        print("Loading stations from NWS")
        stations = self.network.nws.getRadarStations()
        if stations:
            return stations

        raise RuntimeError("Could not load stations")

    def getAlerts(self) -> Dict[AlertType, List[Alert]] | None:
        return self.network.nws.getAlerts()
