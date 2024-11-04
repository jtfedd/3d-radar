from typing import List

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.record import Record
from lib.util.events.listener import Listener


class AnimationManager(Listener):
    def __init__(self, base: ShowBase, state: AppState, events: AppEvents) -> None:
        super().__init__()
        self.state = state
        self.events = events

        self.records: List[Record] = []
        self.index = 0

        self.bind(state.animationRecords, self.setRecords)

        self.listen(
            events.animation.play,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(
            events.input.onPlay,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(events.input.nextFrame, lambda _: self.handleNext(False))
        self.listen(events.input.prevFrame, lambda _: self.handlePrev())

        self.listen(events.animation.next, lambda _: self.handleNext(False))
        self.listen(events.animation.previous, lambda _: self.handlePrev())
        self.listen(events.animation.slider, self.handleSlider)
        self.listen(
            events.requestData, lambda _: state.animationPlaying.setValue(False)
        )

        self.loopDelay = state.loopDelay.value
        self.frameDelay = 1 / state.animationSpeed.value

        self.listen(state.loopDelay, self.updateLoopDelay)
        self.listen(state.animationSpeed, self.updateFrameDelay)

        self.taskTime = 0.0
        self.animationTimer = 0.0
        self.updateTask = base.taskMgr.add(self.update, "animation-update")
        self.listen(state.animationPlaying, lambda _: self.resetAnimationTimer())

    def updateLoopDelay(self, value: float) -> None:
        self.loopDelay = value

    def updateFrameDelay(self, value: int) -> None:
        self.frameDelay = 1 / value

    def resetAnimationTimer(self) -> None:
        self.animationTimer = 0

    def update(self, task: Task) -> int:
        dt = task.time - self.taskTime
        self.taskTime = task.time

        if not self.state.animationPlaying.value:
            return task.cont

        self.animationTimer -= dt
        if self.animationTimer < 0:
            self.handleNext(True)
            if self.index == len(self.records) - 1:
                self.animationTimer = max(self.loopDelay, self.frameDelay)
            else:
                self.animationTimer = self.frameDelay

        return task.cont

    def setRecords(self, records: List[Record]) -> None:
        self.records = records
        if len(self.records) == 0:
            return

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

    def handleNext(self, continuePlaying: bool) -> None:
        if not continuePlaying:
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
        if len(self.records) == 0:
            self.setFrame(None)
            return

        value *= len(self.records) - 1
        self.index = int(round(value))
        self.setFrame(self.records[self.index].key())

    def destroy(self) -> None:
        self.updateTask.cancel()
