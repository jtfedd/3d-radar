from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent

from .keybinding import KeybindingInput
from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(
            UIScaleInput(
                self.root,
                ctx,
                state,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Keybindings"))

        self.addComponent(
            KeybindingInput(self.root, ctx, "Hide UI:", state.hideKeybinding)
        )

    def headerText(self) -> str:
        return "Settings"
