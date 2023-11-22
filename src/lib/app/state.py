import json

from lib.util.events.observable import Observable


class AppState:
    def __init__(self) -> None:
        self.uiScale = Observable[float](1.0)

    def toJson(self) -> str:
        return json.dumps(
            {
                "uiscale": self.uiScale.value,
            },
            sort_keys=True,
            indent=4,
        )

    def fromJson(self, jsonStr: str) -> None:
        raw = json.loads(jsonStr)

        if "uiscale" in raw:
            self.uiScale.setValue(raw["uiscale"])

    def destroy(self) -> None:
        self.uiScale.close()
