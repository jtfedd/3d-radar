from typing import Dict

from lib.model.radar_station import RadarStation

from ..util import makeRequest


class NWSProvider:
    HOST = "https://api.weather.gov"

    def getRadarStations(self) -> Dict[str, RadarStation] | None:
        response = makeRequest(
            self.HOST + "/radar/stations",
            params={"stationType": "WSR-88D"},
            timeout=10,
        )
        if not response:
            return None

        responseJson = response.json()

        stations = {}
        for station in responseJson["features"]:
            stationID = station["properties"]["id"]
            name = station["properties"]["name"]
            long = station["geometry"]["coordinates"][0]
            lat = station["geometry"]["coordinates"][1]
            stations[stationID] = RadarStation(stationID, name, lat, long)

        return stations
