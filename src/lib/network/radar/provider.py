import datetime
from typing import List

import pynexrad

from lib.model.convert.scan_from_pynexrad import scanFromLevel2File
from lib.model.record import Record
from lib.model.scan import Scan


class RadarProvider:
    def load(self, record: Record) -> Scan:
        key = record.awsKey()

        print("Fetching from s3:", key)

        level2File = pynexrad.download_nexrad_file(
            record.station,
            record.time.year,
            record.time.month,
            record.time.day,
            key,
        )

        print("Post-processing", key)
        return scanFromLevel2File(record, level2File)

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
