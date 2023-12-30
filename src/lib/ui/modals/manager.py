from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.util.events.listener import Listener

from .core.modal import Modal
from .station_search.modal import StationSearchModal


class ModalManager(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents):
        super().__init__()

        self.ctx = ctx
        self.state = state
        self.events = events

        self.currentModal: Modal | None = None

        self.listen(
            events.ui.modals.stationSearch, lambda _: self.handleStationSearch()
        )

    def closeModal(self) -> None:
        if self.currentModal:
            self.currentModal.destroy()

    def handleStationSearch(self) -> None:
        self.closeModal()

        self.currentModal = StationSearchModal(self.ctx, self.events)

    def destroy(self) -> None:
        super().destroy()

        self.closeModal()
