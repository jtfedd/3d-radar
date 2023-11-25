from lib.app.input.events import InputEvents
from lib.ui.events import UIEvents


class AppEvents:
    def __init__(self) -> None:
        self.ui = UIEvents()
        self.input = InputEvents()

    def destroy(self) -> None:
        self.ui.destroy()
        self.input.destroy()
