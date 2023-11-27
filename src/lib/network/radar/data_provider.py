from abc import ABC, abstractmethod

from lib.model.record import Record
from lib.model.scan import Scan


class DataProvider(ABC):
    @abstractmethod
    def load(self, record: Record) -> Scan:
        pass
