from enum import Enum


class TaskStatus(Enum):
    CANCELLED = -2
    ERROR = -1
    PENDING = 0
    PROCESSING_READY = 1
    PROCESSING = 2
    POSTPROCESSING_READY = 3
    POSTPROCESSING = 4
    COMPLETE = 5
