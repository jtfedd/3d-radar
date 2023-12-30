from lib.util.events.event_dispatcher import EventDispatcher


class ModalEvents:
    def __init__(self) -> None:
        self.stationSearch = EventDispatcher[None]()

    def destroy(self) -> None:
        self.stationSearch.close()
