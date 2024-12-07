from typing import Dict, List

from lib.model.alert import Alert
from lib.model.alert_type import AlertType
from lib.model.geo_point import GeoPoint
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

    def getAlerts(self, alertType: AlertType) -> List[Alert] | None:
        response = makeRequest(
            self.HOST + "/alerts/active",
            params={
                "status": "actual",
                "limit": 500,
                "code": alertType.code(),
            },
            timeout=10,
        )
        if not response:
            return None

        responseJson = response.json()

        features = responseJson["features"]

        alerts = []

        alerts.append(
            Alert(
                alertType,
                "Test Event",
                "Test Area",
                [
                    [
                        GeoPoint(42.1, -93.8),
                        GeoPoint(41.9, -93.4),
                        GeoPoint(41.7, -93.6),
                        GeoPoint(41.7, -93.9),
                        GeoPoint(42.1, -93.8),
                    ]
                ],
                "Test Headline",
                "Test Description",
            )
        )

        for feature in features:
            geometry = feature["geometry"]
            if geometry is None:
                continue

            boundary = []

            if geometry["type"] == "Polygon":
                boundary = self.parsePolygon(geometry["coordinates"])
            elif geometry["type"] == "MultiPolygon":
                boundary = self.parseMultiPolygon(geometry["coordinates"])
            else:
                continue

            event = feature["properties"]["event"]
            area = feature["properties"]["areaDesc"]

            headline = feature["properties"]["headline"]
            description = feature["properties"]["description"]
            if feature["properties"]["instruction"] is not None:
                description += "\n\n" + feature["properties"]["instruction"]

            alerts.append(
                Alert(alertType, event, area, boundary, headline, description)
            )

        return alerts

    def parseMultiPolygon(
        self, multiPoly: List[List[List[List[float]]]]
    ) -> List[List[GeoPoint]]:
        ret = []

        for poly in multiPoly:
            rings = self.parsePolygon(poly)
            for ring in rings:
                ret.append(ring)

        return ret

    def parsePolygon(
        self,
        poly: List[List[List[float]]],
    ) -> List[List[GeoPoint]]:
        ret = []

        for ring in poly:
            coords = []

            for point in ring:
                coords.append(GeoPoint(lon=point[0], lat=point[1]))

            ret.append(coords)

        return ret
