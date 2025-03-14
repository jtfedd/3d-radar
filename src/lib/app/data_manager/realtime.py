from typing import Dict, List, Set

from direct.task.Task import Task
from pynexrad import (
    PyChunk,
    PyChunkIdentifier,
    PyLevel2File,
    convert_chunks,
    download_chunk,
    get_latest_volume,
    list_chunks_in_volume,
)

from lib.app.context import AppContext
from lib.app.logging import newLogger
from lib.app.state import AppState
from lib.util.events.listener import Listener


class RealtimeManager(Listener):
    POLLING_INTERVAL = 5

    def __init__(self, ctx: AppContext, state: AppState) -> None:
        Listener.__init__(self)

        self.ctx = ctx
        self.state = state
        self.log = newLogger("realtime_data")

        self.chunkIDCache: Dict[str, PyChunkIdentifier] = {}
        self.chunkCache: Dict[int, List[PyChunk]] = {}
        self.volumeCache: Dict[int, PyLevel2File] = {}
        self.latestVolume = -1

        self.lastUpdate = 0.0
        self.updateTask = self.ctx.base.taskMgr.add(self.update, "realtime")

        self.nextUpdate = 0.0

        self.active = False
        self.triggerMany(
            [state.station, state.latest],
            self.deactivate,
        )

    def deactivate(self) -> None:
        self.log.info("Deactivating")

        self.chunkIDCache = {}
        self.chunkCache = {}
        self.volumeCache = {}
        self.latestVolume = -1
        self.nextUpdate = 0
        self.active = False

    def activate(self) -> None:
        if not self.state.latest.getValue():
            return

        self.log.info("Activating")
        site = self.state.station.getValue()
        self.latestVolume = get_latest_volume(site)
        self.log.info("Latest volume " + site + " " + str(self.latestVolume))

        # TODO work backward to get all volumes that don't yet exist in archive
        chunkIDs = list_chunks_in_volume(site, self.latestVolume)
        for chunkID in chunkIDs:
            self.log.info("Chunk: " + chunkID.name)
            self.chunkIDCache[chunkID.name] = chunkID
            self.getChunk(chunkID)

        self.nextUpdate = self.POLLING_INTERVAL

        self.active = True

    def update(self, task: Task) -> int:
        dt = task.time - self.lastUpdate
        self.lastUpdate = task.time

        if not self.active:
            return task.cont

        self.nextUpdate -= dt
        if self.nextUpdate > 0:
            return task.cont

        self.poll()
        self.nextUpdate = self.POLLING_INTERVAL

        return task.cont

    def poll(self) -> None:
        self.log.info("POLLING")

        volumesToRefresh: Set[int] = set()

        site = self.state.station.getValue()
        chunkIDs = list_chunks_in_volume(site, self.latestVolume)
        for chunkID in chunkIDs:
            if chunkID.name in self.chunkIDCache:
                continue

            volumesToRefresh.add(chunkID.volume)

            self.chunkIDCache[chunkID.name] = chunkID
            self.log.info("Chunk: " + chunkID.name)

            if chunkID.name.endswith("E"):
                self.latestVolume += 1
                if self.latestVolume == 1000:
                    self.latestVolume = 1

        for volumeID in volumesToRefresh:
            self.log.info("Recalculate volume " + str(volumeID))

            updatedVolume = convert_chunks(self.chunkCache[volumeID])
            self.log.info("Updated Volume" + str(volumeID))
            self.log.info("REF " + str(len(updatedVolume.reflectivity)))
            self.log.info("VEL " + str(len(updatedVolume.velocity)))

            self.volumeCache[volumeID] = updatedVolume

    def getChunk(self, chunkID: PyChunkIdentifier) -> None:
        if chunkID.volume not in self.chunkCache:
            self.chunkCache[chunkID.volume] = []

        chunk = download_chunk(chunkID)
        self.log.info("Downloaded " + chunkID.name)

        self.chunkCache[chunkID.volume].append(chunk)

    def destroy(self) -> None:
        Listener.destroy(self)
        self.updateTask.cancel()
