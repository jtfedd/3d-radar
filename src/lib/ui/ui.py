from lib.ui.core.config import UIConfig
from lib.ui.footer.footer import Footer


class UI:
    def __init__(self, config: UIConfig) -> None:
        self.config = config

        self.footer = Footer(self.config)

    def destroy(self) -> None:
        self.footer.destroy()
