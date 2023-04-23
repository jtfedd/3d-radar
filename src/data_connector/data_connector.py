from src.data_connector.s3_data_connector import S3DataConnector
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
    
    def loadCached(self, key):
        filePath = self.getFilepath(key)

        if not os.path.exists(filePath):
            return None, False

        print('Reading', filePath)
        
        with open(filePath, 'rb') as f:
            data = pickle.load(f)
        
        print('Read', filePath)

        return data, True
    
    def saveCached(self, key, data):
        filePath = self.getFilepath(key)

        print('Writing', filePath)

        with open(filePath, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

        print('Wrote', filePath)
