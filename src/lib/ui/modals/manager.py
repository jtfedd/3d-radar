from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.util.events.listener import Listener

from .alert.modal import AlertModal
from .alerts.modal import AlertsModal
from .core.modal import Modal
from .license.modal import LicenseModal
from .maptiler.modal import MapTilerModal
from .marker_search.modal import MarkerSearchModal
from .station_search.modal import StationSearchModal
from .timezone_search.modal import TimezoneSearchModal


class ModalManager(Listener):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents):
        super().__init__()
        self.ctx = ctx
        self.state = state
        self.events = events

        self.currentModal: Modal | None = None

        self.listen(
            events.ui.modals.stationSearch,
            lambda _: self.openStationSearch(),
        )

        self.listen(
            events.ui.modals.timeZoneSearch,
            lambda _: self.openTimezoneSearch(),
        )

        self.listen(
            events.ui.modals.markerAdd,
            lambda _: self.openMarkerSearch(),
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
            lambda alert: self.openModal(AlertModal(ctx, events, alert)),
        )

    def openStationSearch(self) -> None:
        if self.state.maptilerKey.value == "":
            self.openModal(
                MapTilerModal(
                    self.ctx,
                    self.state,
                    self.events,
                    self.events.ui.modals.stationSearch,
                )
            )
        else:
            self.openModal(StationSearchModal(self.ctx, self.events))

    def openTimezoneSearch(self) -> None:
        if self.state.maptilerKey.value == "":
            self.openModal(
                MapTilerModal(
                    self.ctx,
                    self.state,
                    self.events,
                    self.events.ui.modals.timeZoneSearch,
                )
            )
        else:
            self.openModal(TimezoneSearchModal(self.ctx, self.events))

    def openMarkerSearch(self) -> None:
        if self.state.maptilerKey.value == "":
            self.openModal(
                MapTilerModal(
                    self.ctx,
                    self.state,
                    self.events,
                    self.events.ui.modals.markerAdd,
                )
            )
        else:
            self.openModal(MarkerSearchModal(self.ctx, self.events))

    def openModal(self, modal: Modal) -> None:
        self.closeModal()
        self.currentModal = modal

    def closeModal(self) -> None:
        if self.currentModal and not self.currentModal.closed:
            self.currentModal.destroy()

    def destroy(self) -> None:
        super().destroy()

        self.closeModal()
