import datetime
from typing import List

import pynexrad

from lib.app.logging import newLogger
from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta


def sweepMetaFromSweep(sweep: pynexrad.Sweep, offset: int) -> SweepMeta:
    return SweepMeta(
        sweep.elevation,
        sweep.az_first,
        sweep.az_step,
        sweep.az_count,
        sweep.range_first,
        sweep.range_step,
        sweep.range_count,
        offset,
    )


def scanDataFromSweeps(sweeps: List[pynexrad.Sweep]) -> ScanData:
    data = bytearray()

    result = []
    offset = 0
    for meta in sweeps:
        result.append(sweepMetaFromSweep(meta, offset))
        data += bytearray(meta.data)
        offset += len(meta.data)

    return ScanData(result, data)


def scanFromLevel2File(record: Record, file: pynexrad.Level2File) -> Scan:
    return Scan(
        record,
        scanDataFromSweeps(file.reflectivity),
        scanDataFromSweeps(file.velocity),
    )


class RadarProvider:
    def __init__(self) -> None:
        self.log = newLogger("radar_provider")

    def load(self, record: Record) -> Scan:
        key = record.awsKey()

        self.log.info(f"Fetching from s3: {key}")

        level2File = pynexrad.download_nexrad_file(key)

        self.log.info(f"Post-processing {key}")
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
