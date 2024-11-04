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
            self.assertStatus(TaskStatus.PENDING)
            self._status = TaskStatus.PROCESSING_READY

    def processing(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self.assertStatus(TaskStatus.PROCESSING_READY)
            self._status = TaskStatus.PROCESSING

    def processingComplete(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self.assertStatus(TaskStatus.PROCESSING)
            self._status = TaskStatus.POSTPROCESSING_READY

    def postprocessingComplete(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self.assertStatus(TaskStatus.POSTPROCESSING)
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
            self.assertStatus(TaskStatus.PROCESSING)

        self.doProcessing()

        self.processingComplete()

    def postProcess(self) -> None:
        if not self.isActive():
            return

        with self.lock:
            self.assertStatus(TaskStatus.POSTPROCESSING_READY)
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

    def assertStatus(self, expectedStatus: TaskStatus) -> None:
        with self.lock:
            if self._status != expectedStatus:
                raise StateError(
                    "Task should be "
                    + str(expectedStatus)
                    + " but is "
                    + str(self._status)
                )

    @abstractmethod
    def name(self) -> str:
        pass
