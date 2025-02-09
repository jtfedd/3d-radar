import json
from collections import defaultdict
from typing import Any, Callable, DefaultDict, Dict, Generic, List, Tuple, TypeVar

from panda3d.core import Vec3

from lib.model.alert_payload import AlertPayload
from lib.model.alert_status import AlertStatus
from lib.model.animation_frame import AnimationFrame
from lib.model.animation_type import AnimationType
from lib.model.data_type import DataType
from lib.model.location_marker import LocationMarker
from lib.model.scan import Scan
from lib.model.time_mode import TimeMode
from lib.util.events.observable import Observable

T = TypeVar("T")
U = TypeVar("U")


class SerializableField(Generic[T, U]):
    def __init__(
        self,
        initialValue: T,
        toJson: Callable[[T], U],
        fromJson: Callable[[U], T],
    ):
        self.observable = Observable[T](initialValue)
        self.toJson = toJson
        self.fromJson = fromJson

    def save(self) -> U:
        return self.toJson(self.observable.value)

    def load(self, value: U) -> None:
        self.observable.setValue(self.fromJson(value))

    def destroy(self) -> None:
        self.observable.close()


def serializeDataType(dataType: DataType) -> int:
    if dataType == DataType.REFLECTIVITY:
        return 0
    if dataType == DataType.VELOCITY:
        return 1

    raise ValueError("Unrecognized data type", dataType)


def deserializeDataType(dataType: int) -> DataType:
    if dataType == 0:
        return DataType.REFLECTIVITY
    if dataType == 1:
        return DataType.VELOCITY

    raise ValueError("Unrecognized data type", dataType)


def serializeTimeMode(timeMode: TimeMode) -> int:
    if timeMode == TimeMode.UTC:
        return 0
    if timeMode == TimeMode.RADAR:
        return 1
    if timeMode == TimeMode.CUSTOM:
        return 2

    raise ValueError("Unrecognized time mode", timeMode)


def deserializeTimeMode(timeMode: int) -> TimeMode:
    if timeMode == 0:
        return TimeMode.UTC
    if timeMode == 1:
        return TimeMode.RADAR
    if timeMode == 2:
        return TimeMode.CUSTOM

    raise ValueError("Unrecognized time mode", timeMode)


def serializeAnimationType(animationType: AnimationType) -> int:
    if animationType == AnimationType.VOLUME:
        return 0
    if animationType == AnimationType.SWEEP:
        return 1

    raise ValueError("Unrecognized animation type")


def deserializeAnimationType(animationType: int) -> AnimationType:
    if animationType == 0:
        return AnimationType.VOLUME
    if animationType == 1:
        return AnimationType.SWEEP

    raise ValueError("Unrecognized animation type", animationType)


class AppState:
    def __init__(self) -> None:
        # Persisted fields
        self.config: Dict[str, SerializableField[Any, Any]] = {}  # type: ignore

        self.uiScale = self.createField("uiScale", 1.0)

        self.useCache = self.createField("useCache", True)
        self.maxCacheSize = self.createField("maxCacheSize", 100)
        self.serializationVersion = self.createField("serializationVersion", -1)

        self.view3D = self.createField("view3D", True)
        self.smooth = self.createField("smooth", True)
        self.volumetricLighting = self.createField("volumetricLighting", False)

        self.showSurfaceLayer = self.createField("showSurfaceLayer", False)
        self.surfaceComposite = self.createField("surfaceComposite", False)
        self.surfaceOpacity = self.createField("surfaceOpacity", 1.0)
        self.surfaceThreshold = self.createField("surfaceThreshold", 0.0)

        self.rMin = self.createField("rMin", 0.04)
        self.rMax = self.createField("rMax", 1.0)
        self.rFalloff = self.createField("rFalloff", 0.7)
        self.rLowCut = self.createField("rLow", 0.0)
        self.rHighCut = self.createField("rHigh", 1.0)

        self.vMin = self.createField("vMin", 0.04)
        self.vMax = self.createField("vMax", 1.0)
        self.vFalloff = self.createField("vFalloff", 0.7)
        self.vLowCut = self.createField("vLow", 0.0)
        self.vHighCut = self.createField("vHigh", 1.0)

        self.ambientLightIntensity = self.createField("ali", 0.2)
        self.directionalLightIntensity = self.createField("dli", 1.0)
        self.directionalLightHeading = self.createField("dlh", 0.625)
        self.directionalLightPitch = self.createField("dlp", 0.5)

        self.timeMode = self.createFieldCustomSerialization(
            "timeMode",
            TimeMode.RADAR,
            serializeTimeMode,
            deserializeTimeMode,
        )

        self.timeFormat = self.createField("timeFormat", True)
        self.timeZone = self.createField("timeZone", "America/Chicago")

        self.station = self.createField("station", "KDMX")
        self.latest = self.createField("latest", True)
        self.year = self.createField("year", 2023)
        self.month = self.createField("month", 11)
        self.day = self.createField("day", 27)
        self.time = self.createField("time", "11:24 AM")
        self.loopMinutes = self.createField("loopMinutes", 30)

        self.mapLatLon = self.createField("mapLatLon", True)
        self.mapStates = self.createField("mapStates", True)
        self.mapCounties = self.createField("mapCounties", True)
        self.mapRoads = self.createField("mapRoads", True)

        self.warningsOpacity = self.createField("warningsOpacity", 1.0)
        self.showTornadoWarnings = self.createField("showTOW", True)
        self.showSevereThunderstormWarnings = self.createField("showSVW", True)

        self.showStations = self.createField("showStations", True)
        self.show3dMarkers = self.createField("show3dMarkers", False)
        self.mapMarkers: Observable[List[LocationMarker]] = (
            self.createFieldCustomSerialization(
                "mapMarkers",
                [],
                lambda rawL: list(map(lambda loc: loc.toJson(), rawL)),
                lambda jsonL: list(map(LocationMarker.fromJson, jsonL)),
            )
        )

        self.animationType = self.createFieldCustomSerialization(
            "animationType",
            AnimationType.SWEEP,
            serializeAnimationType,
            deserializeAnimationType,
        )
        self.animationSpeed = self.createField("animationSpeed", 10)
        self.loopDelay = self.createField("loopDelay", 1.0)

        self.hideKeybinding = self.createField("hideKeybinding", "h")
        self.playKeybinding = self.createField("playKeybinding", "space")
        self.nextKeybinding = self.createField("nextKeybinding", ".")
        self.prevKeybinding = self.createField("prevKeybinding", ",")
        self.stationsButtonKeybinding = self.createField(
            "stationButtonsKeybinding", "s"
        )

        self.dataType = self.createFieldCustomSerialization(
            "dataType",
            DataType.REFLECTIVITY,
            serializeDataType,
            deserializeDataType,
        )

        # Ephemeral fields
        self.state: List[Observable[Any]] = []  # type: ignore

        self.cacheSize = Observable[int](0)

        self.animationFrame = Observable[str | None](None)
        self.animationFrames = Observable[List[AnimationFrame]]([])
        self.animationData = Observable[DefaultDict[str, Scan | None]](
            defaultdict(lambda: None)
        )

        self.animationPlaying = Observable[bool](False)
        self.animationBounds = Observable[Tuple[int, int]]((0, 0))
        self.animationTime = Observable[float](0.0)

        self.loadingData = Observable[bool](False)

        self.alerts = Observable[AlertPayload](
            AlertPayload(status=AlertStatus.READY, alerts={})
        )

        self.directionalLightDirection = Observable[Vec3](Vec3(0, 0, 0))

    def use24HourTime(self) -> bool:
        return self.timeMode.value == TimeMode.UTC or not self.timeFormat.value

    def toJson(self) -> str:
        raw: Dict[str, Any] = {}  # type:ignore

        for item in self.config.items():
            raw[item[0]] = item[1].save()

        return json.dumps(
            raw,
            sort_keys=True,
            indent=4,
        )

    def fromJson(self, jsonStr: str) -> None:
        try:
            raw = json.loads(jsonStr)
        except json.JSONDecodeError:
            return

        for item in self.config.items():
            if item[0] in raw:
                try:
                    item[1].load(raw[item[0]])
                except ValueError:
                    continue

    def createField(self, name: str, initialValue: T) -> Observable[T]:
        field = SerializableField[T, T](
            initialValue,
            fromJson=lambda t: t,
            toJson=lambda t: t,
        )
        self.config[name] = field
        return field.observable

    def createFieldCustomSerialization(
        self,
        name: str,
        initialValue: T,
        toJson: Callable[[T], U],
        fromJson: Callable[[U], T],
    ) -> Observable[T]:
        field = SerializableField[T, U](
            initialValue,
            toJson,
            fromJson,
        )
        self.config[name] = field
        return field.observable

    def destroy(self) -> None:
        for field in self.config.values():
            field.destroy()

        for observable in self.state:
            observable.close()
