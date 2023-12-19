from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable

from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)
        self.ctx = ctx
        self.events = events

        self.listener = Listener()

        self.addComponent(SpacerComponent(self.root))

        scaleInput = self.addComponent(
            UIScaleInput(
                self.root,
                ctx,
                state,
                events,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Keybindings"))

        hideKey = self.addKeybindingInput("Hide UI:", state.hideKeybinding)
        playKey = self.addKeybindingInput("Play/Pause:", state.playKeybinding)
        prevKey = self.addKeybindingInput("Previous Frame:", state.prevKeybinding)
        nextKey = self.addKeybindingInput("Next Frame:", state.nextKeybinding)

        self.setupFocusLoop(
            [
                scaleInput.input.input,
                hideKey.input,
                playKey.input,
                prevKey.input,
                nextKey.input,
            ]
        )

    def addKeybindingInput(
        self,
        label: str,
        observable: Observable[str],
    ) -> PanelTextInput:
        textInput = self.addComponent(
            PanelTextInput(
                self.root,
                self.ctx,
                self.events,
                label,
                observable.value,
                UIConstants.panelContentWidth / 6,
            )
        )

        self.listener.listen(textInput.onChange, observable.setValue)
        self.listener.listen(observable, textInput.input.setText)

        return textInput

    def headerText(self) -> str:
        return "Settings"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
