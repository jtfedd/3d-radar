from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.time_mode import TimeMode
from lib.ui.context import UIContext
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button_group import PanelButtonGroup
from lib.ui.panels.components.spacer import SpacerComponent
from lib.ui.panels.components.text import PanelText
from lib.ui.panels.components.text_input import PanelTextInput
from lib.ui.panels.components.title import TitleComponent
from lib.ui.panels.core.panel_content import PanelContent
from lib.util.events.listener import Listener
from lib.util.events.observable import Observable

from .ui_scale import UIScaleInput


class SettingsPanel(PanelContent):
    MIN_ANIMATION_SPEED = 1
    MAX_ANIMATION_SPEED = 30

    MAX_LOOP_DELAY = 10.0

    def __init__(self, ctx: UIContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)
        self.ctx = ctx
        self.events = events
        self.state = state

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

        self.addComponent(TitleComponent(self.root, ctx, "Animation"))

        self.animationSpeedInput = self.addComponent(
            PanelTextInput(
                self.root,
                self.ctx,
                self.events,
                "Animation Speed (fps):",
                str(state.animationSpeed.value),
                UIConstants.panelContentWidth / 6,
            )
        )

        self.listener.listen(
            state.animationSpeed,
            lambda value: self.animationSpeedInput.input.setText(str(value)),
        )

        self.listener.listen(
            self.animationSpeedInput.onChange, self.updateAnimationSpeed
        )

        self.loopDelayInput = self.addComponent(
            PanelTextInput(
                self.root,
                self.ctx,
                self.events,
                "Loop Delay (s):",
                str(state.loopDelay.value),
                UIConstants.panelContentWidth / 6,
            )
        )

        self.listener.listen(
            state.loopDelay,
            lambda value: self.loopDelayInput.input.setText(str(value)),
        )

        self.listener.listen(self.loopDelayInput.onChange, self.updateLoopDelay)

        self.addComponent(TitleComponent(self.root, ctx, "Date And Time"))

        self.addComponent(
            PanelButtonGroup(
                self.root,
                ctx,
                state.timeMode,
                [
                    ("UTC", TimeMode.UTC),
                    ("Radar", TimeMode.RADAR),
                    ("Custom", TimeMode.CUSTOM),
                ],
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.timeModeDescription = self.addComponent(
            PanelText(self.root, ctx, self.timeModeText())
        )

        self.listener.listen(
            state.timeMode,
            lambda _: self.timeModeDescription.updateText(self.timeModeText()),
        )

        self.addComponent(TitleComponent(self.root, ctx, "Keybindings"))

        hideKey = self.addKeybindingInput("Hide UI:", state.hideKeybinding)
        playKey = self.addKeybindingInput("Play/Pause:", state.playKeybinding)
        prevKey = self.addKeybindingInput("Previous Frame:", state.prevKeybinding)
        nextKey = self.addKeybindingInput("Next Frame:", state.nextKeybinding)

        self.setupFocusLoop(
            [
                scaleInput.input.input,
                self.animationSpeedInput.input,
                self.loopDelayInput.input,
                hideKey.input,
                playKey.input,
                prevKey.input,
                nextKey.input,
            ]
        )

    def updateAnimationSpeed(self, valueStr: str) -> None:
        try:
            newAnimationSpeed = int(valueStr)
        except ValueError:
            self.animationSpeedInput.input.setText(str(self.state.animationSpeed.value))
            return

        newAnimationSpeed = min(
            self.MAX_ANIMATION_SPEED, max(self.MIN_ANIMATION_SPEED, newAnimationSpeed)
        )

        self.state.animationSpeed.setValue(newAnimationSpeed)

    def updateLoopDelay(self, valueStr: str) -> None:
        try:
            newLoopDelay = float(valueStr)
        except ValueError:
            self.loopDelayInput.input.setText(str(self.state.loopDelay.value))

        newLoopDelay = min(self.MAX_LOOP_DELAY, round(newLoopDelay, 2))

        self.state.loopDelay.setValue(newLoopDelay)

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

    def timeModeText(self) -> str:
        if self.state.timeMode.value == TimeMode.UTC:
            return "All times entered and shown in UTC."
        if self.state.timeMode.value == TimeMode.RADAR:
            return (
                "All times entered and shown in the timezone\n"
                + "for the currently selected radar station."
            )
        if self.state.timeMode.value == TimeMode.CUSTOM:
            return "Enter a timezone or search by location."

        return "Unknown time mode"

    def headerText(self) -> str:
        return "Settings"

    def destroy(self) -> None:
        super().destroy()

        self.listener.destroy()
