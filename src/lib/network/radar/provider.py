import datetime
from typing import List

import boto3
import botocore
import pynexrad
from metpy.io import Level2File

from lib.model.convert.scan_from_metpy import scanFromLevel2Data
from lib.model.convert.scan_from_pynexrad import scanFromLevel2File
from lib.model.record import Record
from lib.model.scan import Scan


class RadarProvider:
    RADAR_BUCKET = "noaa-nexrad-level2"

    def __init__(self) -> None:
        config = botocore.client.Config(
            signature_version=botocore.UNSIGNED, user_agent_extra="Resource"
        )

        self.bucket = boto3.resource("s3", config=config).Bucket(self.RADAR_BUCKET)
        self.client = boto3.client("s3", config=config)

    def load(self, record: Record) -> Scan:
        key = record.awsKey()

        # key = f"{key[4:8]}/{key[8:10]}/{key[10:12]}/{key[0:4]}/{key}"
        print("Fetching from s3:", key)

        level2File = pynexrad.download_nexrad_file(
            record.station,
            record.time.year,
            record.time.month,
            record.time.day,
            record.awsKey(),
        )

        # obj = self.client.get_object(Bucket=self.RADAR_BUCKET, Key=key)
        # data = obj["Body"]

        # print("Parsing", key)
        # level2File = Level2File(data)
        # print("Parsed", key)

        print("Post-processing", key)
        # scan = scanFromLevel2Data(record, level2File)
        scan = scanFromLevel2File(record, level2File)
        print("Post-processing finished", key)

        return scan

    def search(self, record: Record, count: int) -> List[Record]:
        searchTime = record.time.astimezone(datetime.timezone.utc)

        records = self.getScans(
            record.station,
            searchTime.year,
            searchTime.month,
            searchTime.day,
        )

        if len(records) < count:
            previousDay = searchTime - datetime.timedelta(days=1)

            records.extend(
                self.getScans(
                    record.station,
                    previousDay.year,
                    previousDay.month,
                    previousDay.day,
                )
            )

        records = list(filter(lambda r: r.time <= searchTime, records))
        records.sort(key=lambda r: r.time)

        if len(records) <= count:
            return records

        return records[-count:]

    def getScans(self, radar: str, year: int, month: int, day: int) -> List[Record]:
        resp = pynexrad.list_records(radar, year, month, day)

        records = []

        for key in resp:
            record = Record.parse(key)
            if record:
                records.append(record)

        return records
