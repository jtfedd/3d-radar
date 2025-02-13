from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.modals.loading_progress.modal import LoadingProgressModal
from lib.util.events.listener import Listener

from .alert.modal import AlertModal
from .alerts.modal import AlertsModal
from .core.modal import Modal
from .license.modal import LicenseModal
from .marker_search.modal import MarkerSearchModal
from .station_search.modal import StationSearchModal
from .timezone_search.modal import TimezoneSearchModal


class ModalManager(Listener):
    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents):
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

        self.listen(
            events.ui.modals.license,
            lambda _: self.openModal(LicenseModal(ctx, events)),
        )

        self.listen(
            events.ui.modals.alerts,
            lambda _: self.openModal(AlertsModal(ctx, state, events)),
        )

        self.listen(
            events.ui.modals.alert,
            lambda payload: self.openModal(AlertModal(ctx, events, payload)),
        )

        self.listen(
            events.ui.modals.loadingProgress,
            lambda payload: self.openModal(LoadingProgressModal(ctx, events, payload)),
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
