from datetime import timedelta
from typing import List

import fsspec
import pyart

from lib.model.convert.scan_from_pyart import scanFromRadar
from lib.model.record import Record
from lib.model.scan import Scan

from .data_provider import DataProvider


class S3DataProvider(DataProvider):
    def load(self, record: Record) -> Scan:
        key = record.awsKey()
        path = f"s3://noaa-nexrad-level2/{key}"

        print("Fetching radar file", path)
        radar = pyart.io.read_nexrad_archive(path)
        print("Done")

        print("Post-processing", key)
        scan = scanFromRadar(record, radar)
        print("Post-processing finished", key)

        return scan

    def search(self, record: Record, count: int) -> List[Record]:
        records = self.getScans(
            record.station,
            record.time.year,
            record.time.month,
            record.time.day,
        )

        if len(records) < count:
            previousDay = record.time - timedelta(days=1)

            records.extend(
                self.getScans(
                    record.station,
                    previousDay.year,
                    previousDay.month,
                    previousDay.day,
                )
            )

        records = list(filter(lambda r: r.time <= record.time, records))
        records.sort(key=lambda r: r.time)

        if len(records) <= count:
            return records

        return records[-count:]

    def getScans(self, radar: str, year: int, month: int, day: int) -> List[Record]:
        prefix = Record.PREFIX_FMT.format(radar, year, month, day)
        pattern = "s3://noaa-nexrad-level2/" + prefix + "*"

        fs = fsspec.filesystem("s3", anon=True)
        files = sorted(fs.glob(pattern))

        records = []

        for f in files:
            record = Record.parse(f[19:])
            if record:
                records.append(record)

        return records
