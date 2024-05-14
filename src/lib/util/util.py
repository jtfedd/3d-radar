def nextPowerOf2(n: int) -> int:
    return 2 ** (n - 1).bit_length()  # type: ignore
