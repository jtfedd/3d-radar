from abc import ABC, abstractmethod


class DataProvider(ABC):
    @abstractmethod
    def load(self, request):
        pass
