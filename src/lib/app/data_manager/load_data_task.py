from typing import Callable

from lib.app.task.task import AbstractTask
from lib.model.record import Record
from lib.model.scan import Scan
from lib.services.radar.radar_service import RadarService
from lib.util.optional import unwrap


class LoadDataTask(AbstractTask):
    def __init__(
        self,
        radarService: RadarService,
        record: Record,
        onDataReceived: Callable[[Scan], None],
    ) -> None:
        super().__init__()

        self.radarService = radarService
        self.record = record

        self.resultData: Scan | None = None
        self.onDataReceived = onDataReceived

        self.readyForProcessing()

    def doProcessing(self) -> None:
        self.resultData = self.radarService.load(self.record)

    def doPostProcessing(self) -> None:
        self.onDataReceived(unwrap(self.resultData))

    def name(self) -> str:
        return "load data " + self.record.key()
