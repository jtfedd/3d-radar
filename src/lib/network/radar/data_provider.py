from abc import ABC, abstractmethod
from typing import List

from lib.model.record import Record
from lib.model.scan import Scan


class DataProvider(ABC):
    @abstractmethod
    def load(self, record: Record) -> Scan:
        pass

    @abstractmethod
    def search(self, record: Record, count: int) -> List[Record]:
        pass
