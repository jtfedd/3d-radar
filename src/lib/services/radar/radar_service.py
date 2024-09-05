from typing import List

import blosc

from lib.app.files.manager import FileManager
from lib.app.files.serialization import deserializeScan, serializeScan
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
        scan = self.loadFromCache(record)
        if scan is not None:
            return scan

        scan = self.network.radar.load(record)

        self.saveToCache(scan)

        return scan

    def loadFromCache(self, record: Record) -> Scan | None:
        compressed = self.fileManager.readCacheFile(record.key())
        if compressed is None:
            return None

        decompressed = blosc.decompress(compressed)
        scan, _ = deserializeScan(decompressed, 0)

        return scan

    def saveToCache(self, scan: Scan) -> None:
        decompressed = serializeScan(scan)
        compressed = blosc.compress(decompressed)

        self.fileManager.saveCacheFile(scan.record.key(), compressed)
