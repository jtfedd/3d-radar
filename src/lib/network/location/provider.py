from typing import List

from lib.model.location import Location

from ..util import makeRequest


class LocationProvider:
    HOST = "https://nominatim.openstreetmap.org"

    def search(self, address: str, limit: int = 1) -> List[Location] | None:
        response = makeRequest(
            self.HOST + "/search",
            params={
                "q": address,
                "format": "geocodejson",
                "addressdetails": 1,
                "countrycodes": "us",
                "limit": limit,
            },
            timeout=10,
        )
        if not response:
            return None

        responseJson = response.json()

        locations = []
        for location in responseJson["features"]:
            details = location["properties"]["geocoding"]

            addressParts = []
            areaParts = []

            if "name" in details:
                addressParts.append(details["name"])
            if "housenumber" in details and "street" in details:
                addressParts.append(f"{details['housenumber']} {details['street']}")
            elif "street" in details:
                addressParts.append(details["street"])
            if "city" in details:
                areaParts.append(details["city"])
            if "state" in details:
                areaParts.append(details["state"])

            addr = ", ".join(addressParts)
            area = ", ".join(areaParts)

            if "postcode" in details:
                area = " ".join([area, details["postcode"]])

            locations.append(
                Location(
                    addr,
                    area,
                    float(location["geometry"]["coordinates"][1]),
                    float(location["geometry"]["coordinates"][0]),
                )
            )

        return locations
