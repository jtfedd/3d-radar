import json

from lib.util.events.observable import Observable


class AppState:
    def __init__(self) -> None:
        self.uiScale = Observable[float](1.0)

        self.volumeMin = Observable[float](0.0)
        self.volumeMax = Observable[float](1.0)
        self.volumeFalloff = Observable[float](0.6)

    def toJson(self) -> str:
        return json.dumps(
            {
                "uiscale": self.uiScale.value,
                "volumemin": self.volumeMin.value,
                "volumemax": self.volumeMax.value,
                "volumefalloff": self.volumeFalloff.value,
            },
            sort_keys=True,
            indent=4,
        )

    def fromJson(self, jsonStr: str) -> None:
        raw = json.loads(jsonStr)

        if "uiscale" in raw:
            self.uiScale.setValue(raw["uiscale"])
        if "volumemin" in raw:
            self.volumeMin.setValue(raw["volumemin"])
        if "volumemax" in raw:
            self.volumeMax.setValue(raw["volumemax"])
        if "volumefalloff" in raw:
            self.volumeFalloff.setValue(raw["volumefalloff"])

    def destroy(self) -> None:
        self.uiScale.close()
        self.volumeMin.close()
        self.volumeMax.close()
        self.volumeFalloff.close()
