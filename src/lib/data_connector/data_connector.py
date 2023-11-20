import os
from typing import Optional

import blosc

from lib.data_provider.abstract_data_provider import AbstractDataProvider
from lib.model.convert.serialization import deserializeScan, serializeScan
from lib.model.record import Record
from lib.model.scan import Scan


class DataConnector:
    def __init__(
        self,
        provider: AbstractDataProvider,
        cacheDir: str,
        useCaching: bool = True,
    ):
        self.provider = provider
        self.cacheDir = cacheDir
        self.useCaching = useCaching

    def load(self, record: Record) -> Scan:
        scan = self.loadCached(record)
        if scan:
            return scan

        scan = self.provider.load(record)
        self.saveCached(record, scan)

        return scan

    def getFilepath(self, record: Record) -> str:
        fileName = record.cacheKey() + ".dat"
        return os.path.join(self.cacheDir, fileName)

    def loadCached(self, record: Record) -> Optional[Scan]:
        if not self.useCaching:
            return None

        filePath = self.getFilepath(record)

        if not os.path.exists(filePath):
            return None

        print("Reading", filePath)

        with open(filePath, "rb") as file:
            data = file.read()

        decompressed = blosc.decompress(data)
        scan, _ = deserializeScan(decompressed)

        print("Read", filePath)

        return scan

    def saveCached(self, record: Record, scan: Scan) -> None:
        if not self.useCaching:
            return

        filePath = self.getFilepath(record)

        print("Writing", filePath)

        data = serializeScan(scan)
        compressed = blosc.compress(data)

        with open(filePath, "wb") as file:
            file.write(compressed)

        print("Wrote", filePath)
