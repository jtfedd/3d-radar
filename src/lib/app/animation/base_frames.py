from typing import List

from lib.model.animation_frame import AnimationFrame
from lib.model.data_type import DataType
from lib.model.scan import Scan


def createBaseFrames(scans: List[Scan], dataType: DataType) -> List[AnimationFrame]:
    frames = []
    for scan in scans:
        sweeps = scan.getSweeps(dataType)
        minEl = min(map(lambda sweep: sweep.elevation, sweeps))

        # Take each sweep at the minimum elevation as its own frame
        for sweep in sweeps:
            if sweep.elevation == minEl:
                frames.append(AnimationFrame([sweep]))

    return sorted(frames, key=lambda frame: frame.startTime)
