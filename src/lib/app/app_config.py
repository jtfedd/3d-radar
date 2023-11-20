import json


class AppConfig:
    def __init__(self) -> None:
        self.uiScale = 1.0

    def toJson(self) -> str:
        return json.dumps(
            {
                "uiscale": self.uiScale,
            },
            sort_keys=True,
            indent=4,
        )

    def fromJson(self, jsonStr: str) -> None:
        raw = json.loads(jsonStr)

        if "uiscale" in raw:
            self.uiScale = raw["uiscale"]
