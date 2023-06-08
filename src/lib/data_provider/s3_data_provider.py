import boto3
import botocore
from metpy.io import Level2File

from lib.data_provider.abstract_data_provider import AbstractDataProvider
from lib.model.from_metpy.scan_from_metpy import scanFromLevel2Data


class S3DataProvider(AbstractDataProvider):
    def __init__(self):
        config = botocore.client.Config(
            signature_version=botocore.UNSIGNED, user_agent_extra="Resource"
        )
        s3 = boto3.resource("s3", config=config)

        self.bucket = s3.Bucket("noaa-nexrad-level2")

    def load(self, record):
        key = record.awsKey()
        print("Fetching from s3:", key)

        # There may be multiple matching objects because file formats have changed in
        # the past. The key should be unique enough to guarantee that any duplicates are
        # different formats of the same data. We should be fine to load the first one.
        obj = list(self.bucket.objects.filter(Prefix=key))[0]
        print("Reading from s3:", obj.key)

        data = obj.get()
        print("Fetched", obj.key)

        print("Parsing", key)
        f = Level2File(data["Body"])
        print("Parsed", key)

        print("Post-processing", key)
        scan = scanFromLevel2Data(record, f)
        print("Post-processing finished", key)

        return scan
