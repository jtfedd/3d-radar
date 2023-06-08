import os

import blosc

from lib.model.serialization.serialization import deserializeScan, serializeScan


class DataConnector:
    def __init__(self, provider, useCaching=True):
        scriptDir = os.path.abspath(os.path.dirname(__file__))
        self.cacheDir = os.path.join(scriptDir, "cached_data")

        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)

        self.provider = provider
        self.useCaching = useCaching

    def load(self, record):
        scan, cached = self.loadCached(record)
        if cached:
            return scan

        scan = self.provider.load(record)
        self.saveCached(record, scan)

        return scan

    def getFilepath(self, record):
        fileName = record.cacheKey() + ".dat"
        return os.path.join(self.cacheDir, fileName)

    def loadCached(self, record):
        if not self.useCaching:
            return None, False

        filePath = self.getFilepath(record)

        if not os.path.exists(filePath):
            return None, False

        print("Reading", filePath)

        with open(filePath, "rb") as f:
            compressed_data = f.read()

        decompressed_data = blosc.decompress(compressed_data)
        scan, _ = deserializeScan(decompressed_data)

        print("Read", filePath)

        return scan, True

    def saveCached(self, record, scan):
        if not self.useCaching:
            return

        filePath = self.getFilepath(record)

        print("Writing", filePath)

        decompressed_data = serializeScan(scan)
        compressed_data = blosc.compress(decompressed_data)

        with open(filePath, "wb") as f:
            f.write(compressed_data)

        print("Wrote", filePath)
