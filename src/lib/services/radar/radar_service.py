from pathlib import Path
from typing import List, Optional

import blosc

from lib.app.files.manager import FileManager
from lib.model.convert.serialization import deserializeScan, serializeScan
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
        # scan = self.loadCached(record)
        # if scan:
        #     return scan

        scan = self.network.radar.load(record)
        # self.saveCached(record, scan)

        return scan

    def getFilepath(self, record: Record) -> Path:
        fileName = record.key() + ".dat"
        return self.fileManager.getCacheFile(fileName)

    def loadCached(self, record: Record) -> Optional[Scan]:
        filePath = self.getFilepath(record)

        if not filePath.exists():
            return None

        print("Reading", filePath)

        with filePath.open("rb") as file:
            data = file.read()

        decompressed = blosc.decompress(data)
        scan, _ = deserializeScan(decompressed)

        print("Read", filePath)

        return scan

    def saveCached(self, record: Record, scan: Scan) -> None:
        filePath = self.getFilepath(record)

        print("Writing", filePath)

        data = serializeScan(scan)
        compressed = blosc.compress(data)

        with filePath.open("wb") as file:
            file.write(compressed)

        print("Wrote", filePath)
