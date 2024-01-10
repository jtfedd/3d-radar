from lib.model.record import Record
from lib.model.scan_data import ScanData


class Scan:
    def __init__(
        self,
        record: Record,
        reflectivity: ScanData,
        velocity: ScanData,
    ):
        self.record = record

        self.reflectivity = reflectivity
        self.velocity = velocity
