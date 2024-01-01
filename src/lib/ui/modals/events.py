from lib.util.events.event_dispatcher import EventDispatcher


class ModalEvents:
    def __init__(self) -> None:
        self.stationSearch = EventDispatcher[None]()
        self.stationSelected = EventDispatcher[str]()

    def destroy(self) -> None:
        self.stationSearch.close()
        self.stationSelected.close()
