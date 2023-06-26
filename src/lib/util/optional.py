from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(optional: Optional[T]) -> T:
    if optional:
        return optional
    raise TypeError("Cannot unwrap None")
