from typing import List

from lib.model.location import Location
from lib.network.network import Network


class LocationService:
    def __init__(self, network: Network) -> None:
        self.network = network

    def search(self, address: str, limit: int = 1) -> List[Location] | None:
        return self.network.locations.search(address, limit)
