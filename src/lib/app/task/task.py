from abc import ABC, abstractmethod

from direct.stdpy.threading import RLock

from lib.util.errors import StateError

from .task_status import TaskStatus


class AbstractTask(ABC):
    def __init__(self) -> None:
        self.lock = RLock()
        self._status = TaskStatus.PENDING

    def getStatus(self) -> TaskStatus:
        with self.lock:
            return self._status

    def readyForProcessing(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.PENDING:
                raise StateError(
                    "Task is not pending: Current state " + str(self._status)
                )
            self._status = TaskStatus.PROCESSING_READY

    def processing(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.PROCESSING_READY:
                raise StateError(
                    "Task is not ready for processing: Current state "
                    + str(self._status)
                )
            self._status = TaskStatus.PROCESSING

    def processingComplete(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.PROCESSING:
                raise StateError(
                    "Task is not currently processing: Current state "
                    + str(self._status)
                )
            self._status = TaskStatus.POSTPROCESSING_READY

    def readyForPostProcessing(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.PROCESSING:
                raise StateError(
                    "Task is not processing: Current state " + str(self._status)
                )
            self._status = TaskStatus.POSTPROCESSING_READY

    def postprocessingComplete(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.POSTPROCESSING:
                raise StateError(
                    "Task is not currently postprocessing: Current state "
                    + str(self._status)
                )
            self._status = TaskStatus.COMPLETE

    def cancel(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self._status = TaskStatus.CANCELLED

    def error(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self._status = TaskStatus.ERROR

    def process(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.PROCESSING:
                raise StateError("Task is not processing " + str(self._status))

        self.doProcessing()

        self.processingComplete()

    def postProcess(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            if self._status != TaskStatus.POSTPROCESSING_READY:
                raise StateError(
                    "Task is not ready for post-processing: Current state "
                    + str(self._status)
                )
            self._status = TaskStatus.POSTPROCESSING

        self.doPostProcessing()

        self.postprocessingComplete()

    @abstractmethod
    def doProcessing(self) -> None:
        pass

    @abstractmethod
    def doPostProcessing(self) -> None:
        pass

    def isActive(self) -> bool:
        with self.lock:
            return self._status in (
                TaskStatus.PENDING,
                TaskStatus.PROCESSING_READY,
                TaskStatus.PROCESSING,
                TaskStatus.POSTPROCESSING_READY,
                TaskStatus.POSTPROCESSING,
            )

    @abstractmethod
    def name(self) -> str:
        pass
