from typing import List

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.record import Record
from lib.util.events.listener import Listener


class AnimationManager(Listener):
    def __init__(self, state: AppState, events: AppEvents) -> None:
        super().__init__()
        self.state = state
        self.events = events

        self.records: List[Record] = []
        self.index = 0

        self.listen(
            events.animation.play,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(
            events.input.onPlay,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(events.animation.next, lambda _: self.handleNext())
        self.listen(events.animation.previous, lambda _: self.handlePrev())
        self.listen(events.animation.slider, self.handleSlider)
        self.listen(
            events.requestData, lambda _: state.animationPlaying.setValue(False)
        )

    def setRecords(self, records: List[Record]) -> None:
        self.records = records
        self.index = len(records) - 1
        self.setFrame(self.records[self.index].key())
        self.setSliderValue()

    def setFrame(self, frame: str | None) -> None:
        self.state.animationFrame.setValue(frame)

    def setSliderValue(self) -> None:
        if len(self.records) < 2:
            self.events.animation.animationProgress.send(1)
        else:
            self.events.animation.animationProgress.send(
                self.index / (len(self.records) - 1)
            )

    def handleNext(self) -> None:
        self.state.animationPlaying.setValue(False)

        if len(self.records) == 0:
            self.setFrame(None)
            return

        self.index += 1
        if self.index == len(self.records):
            self.index = 0

        self.setFrame(self.records[self.index].key())
        self.setSliderValue()

    def handlePrev(self) -> None:
        self.state.animationPlaying.setValue(False)

        if len(self.records) == 0:
            self.setFrame(None)
            return

        self.index -= 1
        if self.index < 0:
            self.index = len(self.records) - 1

        self.setFrame(self.records[self.index].key())
        self.setSliderValue()

    def handleSlider(self, value: float) -> None:
        self.state.animationPlaying.setValue(False)

        if len(self.records) == 0:
            self.setFrame(None)
            return

        value *= len(self.records) - 1
        self.index = int(round(value))
        self.setFrame(self.records[self.index].key())
