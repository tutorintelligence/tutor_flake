from abc import ABC
from collections import abc
from typing import Generic, TypeVar


class Foo:
    def __init__(self) -> None:
        super(Foo, self).__init__()  # noqa: TUT510

    def __str__(self) -> str:
        return super().__str__()


x = super(Foo, Foo())


class Bar1(Foo):
    def __init__(self) -> None:  # noqa: TUT511
        self.foo = 4
        super().__init__
        super.__init__()  # type: ignore
        super().foo()  # type: ignore
        super().__post_init__()  # type: ignore

    def __post_init__(self) -> None:  # noqa: TUT511
        self.foo = 4
        super().__post_init__  # type: ignore
        super.__post_init__()  # type: ignore
        super().foo()  # type: ignore
        super().__init__()


class Bar2(Foo):
    def __init__(self) -> None:
        self.foo = 3
        super().__init__()

    def __post_init__(self) -> None:
        self.foo = 3
        super().__post_init__()  # type: ignore


class Bar3:
    """No call to super necessary because not inherited"""

    def __init__(self) -> None:
        self.foo = 3

    def __post_init__(self) -> None:
        self.foo = 3


T = TypeVar("T")
U = TypeVar("U")


class Bar4(abc.Mapping[int, int], ABC, Generic[T, U]):
    def __init__(self) -> None:
        self.foo = 3

    def __post_init__(self) -> None:
        self.foo = 3
