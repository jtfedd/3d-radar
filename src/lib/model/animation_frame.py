from typing import List

from lib.model.sweep import Sweep
from lib.util.uuid import uuid


class AnimationFrame:
    def __init__(
        self,
        sweeps: List[Sweep],
    ) -> None:
        self.startTime = min(sweep.startTime for sweep in sweeps)
        self.endTime = max(sweep.endTime for sweep in sweeps)

        self.id = uuid()
        self.sweeps = [Sweep.empty(0)]
        self.sweeps.extend(sweeps)

        if len(self.sweeps) > 1:
            lastElevationGap = self.sweeps[-1].elevation - self.sweeps[-2].elevation
            self.sweeps.append(
                Sweep.empty(self.sweeps[-1].elevation + lastElevationGap)
            )

    def data(self) -> bytes:
        result = bytearray()
        for sweep in self.sweeps:
            result.extend(sweep.data)
        return bytes(result)

    def getOffsets(self) -> List[int]:
        result = []
        offset = 0
        for sweep in self.sweeps:
            result.append(offset)
            offset += len(sweep.data)
        return result
