class StateError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__("StateError: " + message)


class InvalidArgumentException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__("Invalid Argument: " + message)


class UnsupportedScanException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__("Unsupported Scan Data: " + message)
