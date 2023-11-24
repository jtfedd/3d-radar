import json
from typing import Any, Dict, TypeVar

from lib.util.events.observable import Observable

T = TypeVar("T")


class AppState:
    def __init__(self) -> None:
        self.observables: Dict[str, Observable[Any]] = {}  # type: ignore

        self.uiScale = self.createField("uiScale", 1.0)

        self.volumeMin = self.createField("volumeMin", 0.0)
        self.volumeMax = self.createField("volumeMax", 1.0)
        self.volumeFalloff = self.createField("volumeFalloff", 0.6)

    def toJson(self) -> str:
        raw: Dict[str, Any] = {}  # type:ignore

        for item in self.observables.items():
            raw[item[0]] = item[1].value

        return json.dumps(
            raw,
            sort_keys=True,
            indent=4,
        )

    def fromJson(self, jsonStr: str) -> None:
        raw = json.loads(jsonStr)

        for item in self.observables.items():
            if item[0] in raw:
                item[1].setValue(raw[item[0]])

    def createField(self, name: str, initialValue: T) -> Observable[T]:
        observable = Observable[T](initialValue)
        self.observables[name] = observable
        return observable

    def destroy(self) -> None:
        for observable in self.observables.values():
            observable.close()
