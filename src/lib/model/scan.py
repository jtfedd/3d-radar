from typing import List

from lib.model.data_type import DataType
from lib.model.record import Record
from lib.model.sweep import Sweep


class Scan:
    def __init__(
        self,
        record: Record,
        reflectivity: List[Sweep],
        velocity: List[Sweep],
    ):
        self.record = record

        self.reflectivity = reflectivity
        self.velocity = velocity

    def getSweeps(self, dataType: DataType) -> List[Sweep]:
        if dataType == DataType.REFLECTIVITY:
            return self.reflectivity
        if dataType == DataType.VELOCITY:
            return self.velocity

        raise ValueError("Unsupported data type", dataType)

    def getElevations(self, dataType: DataType) -> List[float]:
        sweeps = self.getSweeps(dataType)
        elevations = set()
        for sweep in sweeps:
            elevations.add(sweep.elevation)
        return sorted(elevations)
