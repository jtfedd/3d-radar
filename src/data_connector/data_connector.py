from src.data_connector.s3_data_connector import S3DataConnector

import blosc
import os
import pickle

class DataConnector:
    def __init__(self):
        scriptDir = os.path.abspath(os.path.dirname(__file__))
        self.cacheDir = os.path.join(scriptDir, 'cached_data')

        if not os.path.exists(self.cacheDir):
            os.makedirs(self.cacheDir)

        self.s3Connector = S3DataConnector()

    def load(self, request):
        data, cached = self.loadCached(request)
        if cached:
            return data

        data = self.s3Connector.load(request)
        self.saveCached(request, data)

        return data

    def getFilepath(self, request):
        fileName = request.cacheKey() + '.pickle'
        return os.path.join(self.cacheDir, fileName)
    
    def loadCached(self, request):
        filePath = self.getFilepath(request)

        if not os.path.exists(filePath):
            return None, False

        print('Reading', filePath)
        
        with open(filePath, 'rb') as f:
            compressed_data = f.read()
        
        decompressed_data = blosc.decompress(compressed_data)
        data = pickle.loads(decompressed_data)
        
        print('Read', filePath)

        return data, True
    
    def saveCached(self, request, data):
        filePath = self.getFilepath(request)

        print('Writing', filePath)

        pickled_data = pickle.dumps(data)
        compressed_data = blosc.compress(pickled_data)

        with open(filePath, 'wb') as f:
            f.write(compressed_data)

        print('Wrote', filePath)
