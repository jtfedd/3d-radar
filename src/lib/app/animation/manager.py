from typing import List

from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task

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

        self.createFrames()
        self.listen(state.animationData, lambda _: self.createFrames())
        self.listen(state.animationType, lambda _: self.createFrames())
        self.listen(state.dataType, lambda _: self.createFrames())

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

    def createVolumeFrames(self, scans: List[Scan]) -> List[AnimationFrame]:
        frames = []
        for scan in scans:
            frames.append(
                AnimationFrame(scan.getSweeps(self.state.dataType.getValue()))
            )

        frames.sort(key=self.getValidTime)
        return frames

    def createSweepFrames(self, scans: List[Scan]) -> List[AnimationFrame]:
        class SweepInfo:
            def __init__(self, sweep: Sweep, elevations: List[float]):
                self.sweep = sweep
                elIndex = elevations.index(sweep.elevation)
                self.coverageStart = 0.0
                self.coverageEnd = 1000.0

                if elIndex > 0:
                    self.coverageStart = (
                        elevations[elIndex - 1] + elevations[elIndex]
                    ) / 2.0
                if elIndex < len(elevations) - 1:
                    self.coverageEnd = (
                        elevations[elIndex + 1] + elevations[elIndex]
                    ) / 2.0

        sweeps: List[SweepInfo] = []
        for scan in scans:
            elevations = scan.getElevations(self.state.dataType.getValue())
            for sweep in scan.getSweeps(self.state.dataType.getValue()):
                sweeps.append(SweepInfo(sweep, elevations))
        sweeps.sort(key=lambda sweep: sweep.sweep.startTime)

        frames: List[AnimationFrame] = []
        currentSweeps: List[Sweep] = []

        for info in sweeps:
            frameSweeps: List[Sweep] = []
            for cSweep in currentSweeps:
                if (
                    cSweep.elevation < info.coverageStart
                    or cSweep.elevation > info.coverageEnd
                ):
                    frameSweeps.append(cSweep)

            frameSweeps.append(info.sweep)
            frameSweeps.sort(key=lambda sweep: sweep.elevation)

            frames.append(AnimationFrame(frameSweeps))
            currentSweeps = frameSweeps.copy()

        return frames

    def createFrames(self) -> None:
        data = self.state.animationData.getValue()

        scans: List[Scan] = []
        for _, scan in data.items():
            if scan is not None:
                scans.append(scan)

        frames = (
            self.createVolumeFrames(scans)
            if self.state.animationType.getValue() == AnimationType.VOLUME
            else self.createSweepFrames(scans)
        )
        self.state.animationFrames.setValue(frames)

    def updateFrame(self) -> None:
        time = self.state.animationTime.getValue()

        validFrame: str | None = None
        for frame in self.state.animationFrames.getValue():
            if self.getValidTime(frame) <= time:
                validFrame = frame.id
            else:
                break

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
