from datetime import datetime

import boto3
import botocore
import fsspec
import numpy as np
import pyart
from metpy.io import Level2File

from lib.model.convert.scan_from_pyart import scanFromRadar

fs = fsspec.filesystem("s3", anon=True)
files = sorted(fs.glob("s3://noaa-nexrad-level2/2013/05/20/KTLX/KTLX20130520_20*"))
print(files)

print("Reading from pyart")
start = datetime.now()
radar = pyart.io.read_nexrad_archive(
    f"s3://{files[3]}", include_fields=["reflectivity", "velocity"]
)
end = datetime.now()
print(end - start)

# print("Reading from metpy")
# start = datetime.now()
# config = botocore.client.Config(
#     signature_version=botocore.UNSIGNED, user_agent_extra="Resource"
# )
# client = boto3.client("s3", config=config)
# obj = client.get_object(Bucket="noaa-nexrad-level2", Key=files[3][19:])
# data = obj["Body"]
# level2File = Level2File(data)
# end = datetime.now()
# print(end - start)

scan = scanFromRadar(None, radar)

print(radar.nsweeps)
for i in range(radar.nsweeps):
    print("Sweep", i)
    sweepSlice = radar.get_slice(i)
    print("Slice", sweepSlice)

    refData = radar.fields["reflectivity"]["data"][sweepSlice]
    velData = radar.fields["velocity"]["data"][sweepSlice]

    print(np.unique(refData))
    print(refData)
    u = np.unique(velData)
    print(np.unique(velData))
    print(velData)

print("debug")
