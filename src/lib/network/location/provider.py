from typing import List

import requests

from lib.model.location import Location


class LocationProvider:
    HOST = "https://nominatim.openstreetmap.org"

    def search(self, address: str, limit: int = 1) -> List[Location] | None:
        try:
            response = requests.get(
                self.HOST + "/search",
                params={
                    "q": address,
                    "format": "jsonv2",
                    "addressdetails": 1,
                    "countrycodes": "us",
                    "limit": limit,
                },
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

        locations = []
        for location in responseJson:
            locations.append(
                Location(
                    location["display_name"],
                    float(location["lat"]),
                    float(location["lon"]),
                )
            )

        return locations
