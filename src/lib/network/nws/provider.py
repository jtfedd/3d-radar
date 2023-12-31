from typing import Dict

import requests

from lib.model.radar_station import RadarStation


class NWSProvider:
    HOST = "https://api.weather.gov"

    def getRadarStations(self) -> Dict[str, RadarStation] | None:
        try:
            response = requests.get(
                self.HOST + "/radar/stations",
                params={"stationType": "WSR-88D"},
                timeout=10,
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            return None
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        except requests.exceptions.RequestException:
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
