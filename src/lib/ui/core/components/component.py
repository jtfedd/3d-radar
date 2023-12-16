from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def destroy(self) -> None:
        pass
