from typing import List

from lib.model.animation_frame import AnimationFrame
from lib.model.data_type import DataType
from lib.model.scan import Scan
from lib.model.sweep import Sweep


def createVolumeFrames(scans: List[Scan], dataType: DataType) -> List[AnimationFrame]:
    frames = []
    for scan in scans:
        sweeps = sorted(scan.getSweeps(dataType), key=lambda sweep: sweep.startTime)
        elevations = set()

        # Take the first sweep at each elevation, removing duplicates
        frameSweeps: List[Sweep] = []
        for sweep in sweeps:
            if sweep.elevation not in elevations:
                frameSweeps.append(sweep)
                elevations.add(sweep.elevation)

        frames.append(AnimationFrame(frameSweeps))

    return sorted(frames, key=lambda frame: frame.startTime)
