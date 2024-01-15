from typing import Set


class FocusManager:
    def __init__(self) -> None:
        self.focusedItems: Set[str] = set()

    def focus(self, item: str, focused: bool) -> None:
        if focused:
            self.focusedItems.add(item)
        elif item in self.focusedItems:
            self.focusedItems.remove(item)

    def focused(self) -> bool:
        return len(self.focusedItems) > 0
