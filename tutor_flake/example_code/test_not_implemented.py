from types import NotImplementedType
from typing import Any, ClassVar

x = NotImplemented  # noqa: TUT520


def __foo__(bar: Any) -> Any:
    return NotImplemented  # noqa: TUT520


class Foo:
    foo: ClassVar[NotImplementedType] = NotImplemented  # noqa: TUT520

    def foo_1(self) -> Any:
        return NotImplemented  # noqa: TUT520

    def foo_2(self) -> Any:
        bar = NotImplemented  # noqa: TUT520
        return bar

    def __ge__(self, other: "Foo") -> bool:
        return NotImplemented
