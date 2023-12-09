from enum import Enum


class DataType(str, Enum):
    REFLECTIVITY = b"REF"
    VELOCITY = b"VEL"
