from typing import List

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
