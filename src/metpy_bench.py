import datetime
import test.testutils.profile as mem_prof

import boto3
import botocore
from metpy.io import Level2File

from lib.model.convert.scan_from_metpy import scanFromLevel2Data
from lib.model.record import Record

MEM_PROF = False

if MEM_PROF:
    mem_prof.start()

start = datetime.datetime.now()

RADAR_BUCKET = "noaa-nexrad-level2"
KEY = "2022/03/05/KDMX/KDMX20220305_233003_V06"

print(datetime.datetime.now(), "reading from s3")

config = botocore.client.Config(
    signature_version=botocore.UNSIGNED, user_agent_extra="Resource"
)

bucket = boto3.resource("s3", config=config).Bucket(RADAR_BUCKET)
client = boto3.client("s3", config=config)

obj = client.get_object(Bucket=RADAR_BUCKET, Key=KEY)
data = obj["Body"]

print(datetime.datetime.now(), "Parsing")
level2File = Level2File(data)

print(datetime.datetime.now(), "Post-processing")
scan = scanFromLevel2Data(
    Record(station="KDMX", time=datetime.datetime.now()), level2File
)

print(datetime.datetime.now(), "done")

print(datetime.datetime.now() - start)

if MEM_PROF:
    mem_prof.stop()

print(len(scan.velocityBytes))
print(len(scan.reflectivityBytes))
