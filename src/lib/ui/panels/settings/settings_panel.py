from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_content import PanelContent
from lib.ui.panels.settings.text_component import TextComponent


class SettingsPanel(PanelContent):
    def __init__(self, config: UIConfig) -> None:
        super().__init__(config)

        for i in range(10):
            text = TextComponent(self.root, config)
            self.componentManager.add(text)

    def headerText(self) -> str:
        return "Settings"
