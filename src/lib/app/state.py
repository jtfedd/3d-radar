import json
from typing import Any, Callable, Dict, Generic, List, TypeVar

from lib.model.data_type import DataType
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


class AppState:
    def __init__(self) -> None:
        # Persisted fields
        self.config: Dict[str, SerializableField[Any, Any]] = {}  # type: ignore

        self.uiScale = self.createField("uiScale", 1.0)

        self.volumeMin = self.createField("volumeMin", 0.04)
        self.volumeMax = self.createField("volumeMax", 1.0)
        self.volumeFalloff = self.createField("volumeFalloff", 0.7)

        self.station = self.createField("station", "KDMX")
        self.year = self.createField("year", 2023)
        self.month = self.createField("month", 11)
        self.day = self.createField("day", 27)
        self.time = self.createField("time", "11:24")
        self.frames = self.createField("frames", 5)

        self.hideKeybinding = self.createField("hideKeybinding", "h")
        self.playKeybinding = self.createField("playKeybinding", "space")

        self.dataType = self.createFieldCustomSerialization(
            "dataType",
            DataType.REFLECTIVITY,
            serializeDataType,
            deserializeDataType,
        )

        # Ephemeral fields
        self.state: List[Observable[Any]] = []  # type: ignore

        self.animationPlaying = Observable[bool](False)
        self.animationFrame = Observable[str | None](None)

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
