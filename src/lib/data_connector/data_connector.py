from lib.model.serialization.serialization import serializeScan, deserializeScan

import blosc
import os

useCaching = False


class DataConnector:
    def __init__(self, provider):
        scriptDir = os.path.abspath(os.path.dirname(__file__))
        self.cacheDir = os.path.join(scriptDir, "cached_data")

        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)

        self.provider = provider

    def load(self, request):
        scan, cached = self.loadCached(request)
        if cached:
            return scan

        scan = self.provider.load(request)
        self.saveCached(request, scan)

        return scan

    def getFilepath(self, request):
        fileName = request.cacheKey() + ".dat"
        return os.path.join(self.cacheDir, fileName)

    def loadCached(self, request):
        if not useCaching:
            return None, False

        filePath = self.getFilepath(request)

        if not os.path.exists(filePath):
            return None, False

        print("Reading", filePath)

        with open(filePath, "rb") as f:
            compressed_data = f.read()

        decompressed_data = blosc.decompress(compressed_data)
        scan, _ = deserializeScan(decompressed_data)

        print("Read", filePath)

        return scan, True

    def saveCached(self, request, scan):
        if not useCaching:
            return

        filePath = self.getFilepath(request)

        print("Writing", filePath)

        decompressed_data = serializeScan(scan)
        compressed_data = blosc.compress(decompressed_data)

        with open(filePath, "wb") as f:
            f.write(compressed_data)

        print("Wrote", filePath)
