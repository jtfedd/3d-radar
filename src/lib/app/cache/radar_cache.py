from typing import Dict

from lib.model.scan import Scan


class RadarCache:
    def __init__(self) -> None:
        self.data: Dict[str, Scan] = {}

    def get(self, key: str) -> Scan | None:
        if key not in self.data:
            return None

        return self.data[key]

    def setData(self, data: Dict[str, Scan]) -> None:
        self.data = data
