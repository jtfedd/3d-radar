from typing import List

from lib.app.files.manager import FileManager
from lib.model.record import Record
from lib.model.scan import Scan
from lib.network.network import Network


class RadarService:
    def __init__(self, fileManager: FileManager, network: Network) -> None:
        self.network = network
        self.fileManager = fileManager

    def search(self, record: Record, count: int) -> List[Record]:
        return self.network.radar.search(record, count)

    def load(self, record: Record) -> Scan:
        return self.network.radar.load(record)
