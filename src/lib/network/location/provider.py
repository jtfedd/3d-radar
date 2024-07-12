from typing import List

from lib.app.state import AppState
from lib.model.location import Location

from ..util import makeRequest


class LocationProvider:
    HOST = "https://api.maptiler.com"

    def __init__(self, state: AppState):
        self.state = state

    def search(self, address: str, limit: int = 1) -> List[Location] | None:
        print("Searching", address)

        response = makeRequest(
            self.HOST + "/geocoding/" + address + ".json",
            params={
                "key": self.state.maptilerKey.value,
                "autocomplete": "false",
                "fuzzyMatch": "false",
                "country": "us",
                "limit": str(limit),
            },
            timeout=10,
        )
        if not response:
            return None

        responseJson = response.json()

        locations = []
        for location in responseJson["features"]:
            context = {}
            if "context" in location:
                for c in location["context"]:
                    t = c["id"].split(".")[0]
                    context[t] = c["text"]

            addressParts = []
            areaParts = []

            if "address" in location and "text" in location:
                addressParts.append(f"{location["address"]} {location["text"]}")
            elif "text" in location:
                addressParts.append(location["text"])
            if "municipality" in context:
                areaParts.append(context["municipality"])
            if "joint_municipality" in context:
                areaParts.append(context["joint_municipality"])
            if "region" in context:
                areaParts.append(context["region"])

            addr = ", ".join(addressParts)
            area = ", ".join(areaParts)

            if "postal_code" in context:
                area = " ".join([area, context["postal_code"]])

            locations.append(
                Location(
                    addr.upper(),
                    area.upper(),
                    float(location["center"][1]),
                    float(location["center"][0]),
                )
            )

        return locations
