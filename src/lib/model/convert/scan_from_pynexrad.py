import numpy as np
import pynexrad

from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.scan_data import ScanData
from lib.model.sweep_meta import SweepMeta


def sweepMetaFromSweep(sweep: pynexrad.Sweep) -> SweepMeta:
    return SweepMeta(
        sweep.elevation,
        sweep.az_first,
        sweep.az_step,
        sweep.az_count,
        sweep.range_first,
        sweep.range_step,
        sweep.range_count,
        sweep.offset,
    )


def scanDataFromScan(scan: pynexrad.Scan) -> ScanData:
    data = np.array(scan.data, dtype=np.float32).tobytes()

    metas = []
    for meta in scan.meta:
        metas.append(sweepMetaFromSweep(meta))

    return ScanData(metas, data)


def scanFromLevel2File(record: Record, file: pynexrad.Level2File) -> Scan:
    return Scan(
        record,
        scanDataFromScan(file.reflectivity),
        scanDataFromScan(file.velocity),
    )
