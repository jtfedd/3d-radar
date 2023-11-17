from typing import List

from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_spacer import PanelSpacer
from lib.ui.panels.components.panel_text_input import PanelTextInput
from lib.ui.panels.core.panel_component import PanelComponent
from lib.ui.panels.core.panel_content import PanelContent


class SettingsPanel(PanelContent):
    def __init__(self, config: UIConfig) -> None:
        super().__init__(config)

        self.components: List[PanelComponent] = []

        self.addComponent(PanelSpacer(self.root))

        self.scaleInput = self.addComponent(
            PanelTextInput(
                self.root,
                config,
                label="UI Scale",
            )
        )

    def headerText(self) -> str:
        return "Settings"

    def destroy(self) -> None:
        super().destroy()

        for component in self.components:
            component.destroy()
