from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_spacer import PanelSpacer
from lib.ui.panels.core.panel_content import PanelContent

from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    def __init__(self, config: UIConfig) -> None:
        super().__init__(config)

        self.addComponent(PanelSpacer(self.root))

        self.scaleInput = self.addComponent(
            UIScaleInput(
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
