from lib.app.events import AppEvents
from lib.ui.context import UIContext
from lib.util.events.listener import Listener

from .core.modal import Modal
from .marker_search.modal import MarkerSearchModal
from .station_search.modal import StationSearchModal
from .timezone_search.modal import TimezoneSearchModal


class ModalManager(Listener):
    def __init__(self, ctx: UIContext, events: AppEvents):
        super().__init__()

        self.currentModal: Modal | None = None

        self.listen(
            events.ui.modals.stationSearch,
            lambda _: self.openModal(StationSearchModal(ctx, events)),
        )

        self.listen(
            events.ui.modals.timeZoneSearch,
            lambda _: self.openModal(TimezoneSearchModal(ctx, events)),
        )

        self.listen(
            events.ui.modals.markerAdd,
            lambda _: self.openModal(MarkerSearchModal(ctx, events)),
        )

    def openModal(self, modal: Modal) -> None:
        self.closeModal()
        self.currentModal = modal

    def closeModal(self) -> None:
        if self.currentModal and not self.currentModal.closed:
            self.currentModal.destroy()

    def destroy(self) -> None:
        super().destroy()

        self.closeModal()
