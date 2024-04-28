from lib.util.events.event_dispatcher import EventDispatcher


class ModalEvents:
    def __init__(self) -> None:
        self.stationSearch = EventDispatcher[None]()
        self.stationSelected = EventDispatcher[str]()

        self.timeZoneSearch = EventDispatcher[None]()
        self.timeZoneSelected = EventDispatcher[str]()

        self.license = EventDispatcher[None]()

        self.alerts = EventDispatcher[None]()

    def destroy(self) -> None:
        self.stationSearch.close()
        self.stationSelected.close()

        self.timeZoneSearch.close()
        self.timeZoneSelected.close()

        self.license.close()

        self.alerts.close()
