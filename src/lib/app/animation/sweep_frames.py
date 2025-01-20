import bisect
from typing import List

from lib.model.animation_frame import AnimationFrame
from lib.model.data_type import DataType
from lib.model.scan import Scan
from lib.model.sweep import Sweep


class SweepInfo:
    def __init__(self, sweep: Sweep, elevations: List[float]):
        self.sweep = sweep
        self.coverageStart = 0.0
        self.coverageEnd = 1000.0

        elIndex = elevations.index(sweep.elevation)
        if elIndex > 0:
            self.coverageStart = (elevations[elIndex - 1] + elevations[elIndex]) / 2.0
        if elIndex < len(elevations) - 1:
            self.coverageEnd = (elevations[elIndex + 1] + elevations[elIndex]) / 2.0


def createSweepFrames(scans: List[Scan], dataType: DataType) -> List[AnimationFrame]:
    sweepInfos: List[SweepInfo] = []
    for scan in scans:
        elevations = scan.getElevations(dataType)
        sweepInfos.extend(
            SweepInfo(sweep, elevations) for sweep in scan.getSweeps(dataType)
        )
    sweepInfos.sort(key=lambda sweep: sweep.sweep.endTime)

    frames: List[AnimationFrame] = []
    currentSweeps: List[Sweep] = []

    for info in sweepInfos:
        currentSweeps = [
            sweep
            for sweep in currentSweeps
            if sweep.elevation < info.coverageStart
            or sweep.elevation > info.coverageEnd
        ]

        bisect.insort(currentSweeps, info.sweep, key=lambda sweep: sweep.elevation)

        frames.append(AnimationFrame(currentSweeps[:]))

    return frames
