import math
from typing import List
from zoneinfo import available_timezones

from lib.app.context import AppContext
from lib.app.events import AppEvents
from lib.app.files.manager import FileManager
from lib.app.focus.focusable import Focusable
from lib.app.state import AppState
from lib.model.time_mode import TimeMode
from lib.ui.core.constants import UIConstants
from lib.ui.panels.components.button import PanelButton
from lib.ui.panels.components.button_group import PanelButtonGroup
from lib.ui.panels.components.checkbox import CheckboxComponent
from lib.ui.panels.components.progress import ProgressComponent
from lib.ui.panels.components.slider import SliderComponent
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

    def __init__(self, ctx: AppContext, state: AppState, events: AppEvents) -> None:
        super().__init__(ctx, state, events)
        self.ctx = ctx
        self.events = events
        self.state = state

        self.listener = Listener()

        self.addComponent(SpacerComponent(self.root))

        self.scaleInput = self.addComponent(
            UIScaleInput(
                self.root,
                ctx,
                state,
                events,
            )
        )

        self.addComponent(TitleComponent(self.root, ctx, "Local Cache"))
        self.addComponent(
            CheckboxComponent(self.root, ctx, "Use Cache", state.useCache)
        )

        cacheSizeSlider = self.addComponent(
            SliderComponent(
                self.root,
                ctx,
                state.maxCacheSize.value,
                (50, 500),
                "Max Size:",
                leftPadding=0.06,
            )
        )

        self.listener.listen(
            cacheSizeSlider.slider.onValueChange,
            lambda value: state.maxCacheSize.setValue(int(value)),
        )

        self.listener.bind(
            state.maxCacheSize,
            lambda value: cacheSizeSlider.label.label.text.setText(
                "Max Size: " + str(value) + "mb"
            ),
        )

        self.cacheUsage = self.addComponent(
            ProgressComponent(
                self.root,
                ctx,
                0,
                "Usage:",
                leftPadding=0.06,
            )
        )

        self.listener.bind(
            state.maxCacheSize,
            lambda _: self.updateCacheUsage(),
        )

        self.listener.bind(
            state.cacheSize,
            lambda _: self.updateCacheUsage(),
        )

        self.addComponent(SpacerComponent(self.root))
        clearCacheButton = self.addComponent(
            PanelButton(root=self.root, ctx=ctx, text="Clear Cache")
        )
        self.listener.listen(clearCacheButton.button.onClick, events.clearCache.send)

        clearCacheButton.button.setDisabled(not state.useCache.value)
        self.listener.listen(
            state.useCache, lambda value: clearCacheButton.button.setDisabled(not value)
        )

        self.addComponent(SpacerComponent(self.root))
        clearAllDataButton = self.addComponent(
            PanelButton(root=self.root, ctx=ctx, text="Clear All Data and Exit")
        )
        self.listener.listen(
            clearAllDataButton.button.onClick, events.clearDataAndExit.send
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

        self.timeSpacer = self.addComponent(SpacerComponent(self.root))

        self.timeZone = self.addComponent(
            PanelTextInput(
                root=self.root,
                ctx=ctx,
                events=events,
                label="Time Zone:",
                initialValue=state.timeZone.value,
                inputWidth=UIConstants.panelContentWidth / 2,
                validationText="Invalid Time Zone",
            )
        )

        self.listener.listen(self.timeZone.input.onChange, self.validateTimeZone)
        self.listener.listen(
            events.ui.modals.timeZoneSelected, self.timeZone.input.setText
        )

        self.timeZoneSpacer = self.addComponent(SpacerComponent(self.root))

        self.searchButton = self.addComponent(
            PanelButton(
                root=self.root,
                ctx=ctx,
                text="Search By Location",
            )
        )

        self.listener.listen(
            self.searchButton.button.onClick, events.ui.modals.timeZoneSearch.send
        )

        self.searchButtonSpacer = self.addComponent(SpacerComponent(self.root))

        self.timeFormat = self.addComponent(
            PanelButtonGroup(
                self.root,
                ctx,
                state.timeFormat,
                [
                    ("12H", True),
                    ("24H", False),
                ],
                label="Time Format:",
                left=3 * UIConstants.panelContentWidth / 4,
                height=UIConstants.panelInputHeight,
            )
        )

        self.addComponent(SpacerComponent(self.root))

        self.addComponent(TitleComponent(self.root, ctx, "Keybindings"))

        self.hideKey = self.addKeybindingInput("Hide UI:", state.hideKeybinding)
        self.playKey = self.addKeybindingInput("Play/Pause:", state.playKeybinding)
        self.prevKey = self.addKeybindingInput("Previous Frame:", state.prevKeybinding)
        self.nextKey = self.addKeybindingInput("Next Frame:", state.nextKeybinding)

        self.updateInputsForTimeMode()
        self.listener.listen(state.timeMode, lambda _: self.updateInputsForTimeMode())

    def updateCacheUsage(self) -> None:
        maxSize = self.state.maxCacheSize.value * FileManager.BYTES_PER_MEGABYTE
        usage = self.state.cacheSize.value

        usageStr = str(int(math.ceil(usage / FileManager.BYTES_PER_MEGABYTE)))

        self.cacheUsage.label.label.updateText("Usage: " + usageStr + "mb")
        self.cacheUsage.progressBar.setProgress(usage / maxSize)

    def updateInputsForTimeMode(self) -> None:
        timeMode = self.state.timeMode.value
        self.timeSpacer.setHidden(timeMode == TimeMode.UTC)
        self.timeFormat.setHidden(timeMode == TimeMode.UTC)
        self.timeZone.setHidden(timeMode != TimeMode.CUSTOM)
        self.timeZoneSpacer.setHidden(timeMode != TimeMode.CUSTOM)
        self.searchButton.setHidden(timeMode != TimeMode.CUSTOM)
        self.searchButtonSpacer.setHidden(timeMode != TimeMode.CUSTOM)

        focusableItems: List[Focusable] = []
        focusableItems.append(self.scaleInput.input.input)
        focusableItems.append(self.animationSpeedInput.input)
        focusableItems.append(self.loopDelayInput.input)

        if timeMode == TimeMode.CUSTOM:
            focusableItems.append(self.timeZone.input)

        focusableItems.append(self.hideKey.input)
        focusableItems.append(self.playKey.input)
        focusableItems.append(self.prevKey.input)
        focusableItems.append(self.nextKey.input)

        self.setupFocusLoop(focusableItems)

    def validateTimeZone(self, tzStr: str) -> None:
        valid = tzStr in available_timezones()
        self.timeZone.setValid(valid)
        if valid:
            self.state.timeZone.setValue(tzStr)

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
