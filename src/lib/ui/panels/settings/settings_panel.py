from lib.ui.core.config import UIConfig
from lib.ui.panels.components.panel_spacer import PanelSpacer
from lib.ui.panels.core.panel_content import PanelContent
from lib.ui.panels.panel_events import PanelEvents

from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    def __init__(self, config: UIConfig, events: PanelEvents) -> None:
        super().__init__(config)

        self.addComponent(PanelSpacer(self.root))

        self.scaleInput = self.addComponent(
            UIScaleInput(
                self.root,
                config,
                label="UI Scale",
            )
        )

        self.scaleSub = self.scaleInput.onScaleChange.listen(events.scaleChanged.send)

    def headerText(self) -> str:
        return "Settings"

    def destroy(self) -> None:
        super().destroy()

        self.scaleSub.cancel()

        for component in self.components:
            component.destroy()
