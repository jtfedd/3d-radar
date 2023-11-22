from lib.app.state import AppState
from lib.ui.core.context import UIContext
from lib.ui.events import UIEvents
from lib.ui.panels.components.panel_spacer import PanelSpacer
from lib.ui.panels.core.panel_content import PanelContent

from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: UIEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(PanelSpacer(self.root))

        self.scaleInput = self.addComponent(
            UIScaleInput(
                self.root,
                ctx,
                state,
                label="UI Scale",
            )
        )

    def headerText(self) -> str:
        return "Settings"

    def destroy(self) -> None:
        super().destroy()

        for component in self.components:
            component.destroy()
