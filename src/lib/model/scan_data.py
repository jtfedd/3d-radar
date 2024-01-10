from typing import List

from lib.model.sweep_meta import SweepMeta


class ScanData:
    def __init__(self, metas: List[SweepMeta], data: bytes):
        self.metas = metas
        self.data = data
