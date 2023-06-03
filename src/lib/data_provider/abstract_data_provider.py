from abc import ABC, abstractmethod


class AbstractDataProvider(ABC):
    @abstractmethod
    def load(self, request):
        pass
