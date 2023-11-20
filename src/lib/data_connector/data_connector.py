from pathlib import Path
from typing import Optional

import blosc

from lib.app.file_manager import FileManager
from lib.data_provider.abstract_data_provider import AbstractDataProvider
from lib.model.convert.serialization import deserializeScan, serializeScan
from lib.model.record import Record
from lib.model.scan import Scan


class DataConnector:
    def __init__(
        self,
        provider: AbstractDataProvider,
        fileManager: FileManager,
        useCaching: bool = True,
    ):
        self.provider = provider
        self.fileManager = fileManager
        self.useCaching = useCaching

    def load(self, record: Record) -> Scan:
        scan = self.loadCached(record)
        if scan:
            return scan

        scan = self.provider.load(record)
        self.saveCached(record, scan)

        return scan

    def getFilepath(self, record: Record) -> Path:
        fileName = record.cacheKey() + ".dat"
        return self.fileManager.getCacheFile(fileName)

    def loadCached(self, record: Record) -> Optional[Scan]:
        if not self.useCaching:
            return None

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
        if not self.useCaching:
            return

        filePath = self.getFilepath(record)

        print("Writing", filePath)

        data = serializeScan(scan)
        compressed = blosc.compress(data)

        with filePath.open("wb") as file:
            file.write(compressed)

        print("Wrote", filePath)
