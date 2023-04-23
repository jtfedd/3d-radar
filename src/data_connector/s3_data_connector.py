import boto3
import botocore

from metpy.io import Level2File

class S3DataConnector:
    def __init__(self):
        config = botocore.client.Config(signature_version=botocore.UNSIGNED, user_agent_extra='Resource')
        s3 = boto3.resource('s3', config=config)

        self.bucket = s3.Bucket('noaa-nexrad-level2')

    def load(self, key):
        print('Fetching from s3:',  key)
        obj = self.bucket.Object(key=key)
        data = obj.get()
        print('Fetched', key)

        print('Parsing', key)
        f = Level2File(data['Body'])
        print('Parsed', key)

        return f