from abc import ABC

class ObjectEquals(ABC):
    def __eq__(self, other):
        if type(other) is not type(self):
            return NotImplemented
        return self.__dict__ == other.__dict__
