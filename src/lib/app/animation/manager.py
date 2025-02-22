import bisect
from typing import List

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

from lib.app.animation.base_frames import createBaseFrames
from lib.app.animation.sweep_frames import createSweepFrames
from lib.app.animation.volume_frames import createVolumeFrames
from lib.app.events import AppEvents
from lib.app.state import AppState
from lib.model.animation_frame import AnimationFrame
from lib.model.animation_type import AnimationType
from lib.model.data_type import DataType
from lib.model.record import Record
from lib.model.scan import Scan
from lib.model.sweep import Sweep
from lib.util.events.listener import Listener


class AnimationManager(Listener):
    def __init__(self, base: ShowBase, state: AppState, events: AppEvents) -> None:
        super().__init__()
        self.state = state
        self.events = events

        self.records: List[Record] = []
        self.index = 0

        self.triggerMany(
            [
                state.animationData,
                state.animationType,
                state.dataType,
                state.view3D,
                state.velComposite,
                state.refComposite,
            ],
            self.createFrames,
            triggerImmediately=True,
        )

        self.listen(
            events.animation.play,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(
            events.input.onPlay,
            lambda _: state.animationPlaying.setValue(not state.animationPlaying.value),
        )

        self.listen(events.input.nextFrame, lambda _: self.handleNext(forward=True))
        self.listen(events.input.prevFrame, lambda _: self.handleNext(forward=False))

        self.listen(events.animation.next, lambda _: self.handleNext(forward=True))
        self.listen(events.animation.previous, lambda _: self.handleNext(forward=False))
        self.listen(
            events.requestData, lambda _: state.animationPlaying.setValue(False)
        )
        self.listen(state.animationPlaying, lambda _: self.resetDelayTimer())

        self.updateFrame()
        self.listen(self.state.animationTime, lambda _: self.updateFrame())
        self.listen(self.state.animationFrames, lambda _: self.updateFrame())

        self.taskTime = 0.0
        self.delayTime = 0.0
        self.updateTask = base.taskMgr.add(self.update, "animation-update")

    def resetDelayTimer(self) -> None:
        self.delayTime = 0

    def update(self, task: Task) -> int:
        dt = task.time - self.taskTime
        self.taskTime = task.time

        if not self.state.animationPlaying.value:
            return task.cont

        start, stop = self.state.animationBounds.getValue()
        animationTime = self.state.animationTime.getValue()

        if self.delayTime > 0 or animationTime >= stop:
            self.delayTime -= dt
            if self.delayTime < 0:
                self.state.animationTime.setValue(start)
            return task.cont

        animationStep = self.state.animationSpeed.getValue() * 60 * dt

        animationTime += animationStep
        if animationTime < stop:
            self.state.animationTime.setValue(animationTime)
            return task.cont

        animationTime = stop
        self.state.animationTime.setValue(animationTime)
        self.delayTime = self.state.loopDelay.getValue()
        return task.cont

    def getDataFromScan(self, scan: Scan) -> List[Sweep]:
        return (
            scan.reflectivity
            if self.state.dataType.getValue() == DataType.REFLECTIVITY
            else scan.velocity
        )

    def createFrames(self) -> None:
        data = self.state.animationData.getValue()

        is3D = self.state.view3D.getValue()
        isComposite = (
            self.state.refComposite.getValue()
            if self.state.dataType.getValue() == DataType.REFLECTIVITY
            else self.state.velComposite.getValue()
        )

        scans: List[Scan] = []
        for _, scan in data.items():
            if scan is not None:
                scans.append(scan)

        frames = []
        if not is3D and not isComposite:
            frames = createBaseFrames(scans, self.state.dataType.getValue())
        elif self.state.animationType.getValue() == AnimationType.VOLUME:
            frames = createVolumeFrames(scans, self.state.dataType.getValue())
        else:
            frames = createSweepFrames(scans, self.state.dataType.getValue())

        self.state.animationFrames.setValue(frames)

    def updateFrame(self) -> None:
        time = self.state.animationTime.getValue()
        frames = self.state.animationFrames.getValue()
        index = bisect.bisect_right(frames, time, key=self.getValidTime) - 1
        validFrame = frames[index].id if index >= 0 else None

        self.state.animationFrame.setValue(validFrame)

    def handleNext(self, forward: bool = True) -> None:
        self.state.animationPlaying.setValue(False)

        currentFrame = self.state.animationFrame.getValue()
        if currentFrame is None:
            return

        frames = self.state.animationFrames.getValue()
        if len(frames) < 2:
            return

        currentIndex = -1
        for i, frame in enumerate(frames):
            if frame.id == currentFrame:
                currentIndex = i
                break

        if currentIndex < 0:
            return

        delta = 1 if forward else -1
        nextFrame = frames[(currentIndex + delta) % len(frames)]
        time = self.getValidTime(nextFrame)
        start, stop = self.state.animationBounds.getValue()
        time = min(stop, max(start, time))
        self.state.animationTime.setValue(time)

    def getValidTime(self, frame: AnimationFrame) -> int:
        return (
            frame.startTime
            if self.state.animationType.getValue() == AnimationType.VOLUME
            else frame.endTime
        )

    def destroy(self) -> None:
        self.updateTask.cancel()
