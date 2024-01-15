from abc import ABC, abstractmethod


class AddressResultsComponent(ABC):
    @abstractmethod
    def height(self) -> float:
        pass

    @abstractmethod
    def destroy(self) -> None:
        pass
