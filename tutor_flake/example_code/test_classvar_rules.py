import dataclasses
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Final, List, NamedTuple, Protocol, TypeVar

from typing_extensions import Self


class DummyClass:

    a: int = 4  # noqa: TUT503
    b: float  # noqa: TUT503
    c = "abc"  # noqa: TUT502
    d = bool  # noqa: TUT502
    e: "str" = "abc"  # noqa: TUT503
    f: ClassVar
    g: ClassVar[bool] = False
    h: ClassVar[List[bool]]
    i: Final = 3
    j: Final[bool] = True

    def __init__(self, value: float) -> None:
        pass

    def __repr__(self) -> str:
        return f"{self.a} {self.b}"

    @classmethod
    def override(cls, new_c: str) -> None:
        cls.c = new_c

    def instance_override(self, new_c: str) -> None:
        # we allow this, but is still bad
        self.c = new_c

    k: ClassVar[bool]  # noqa: TUT501
    m = 3  # noqa: TUT501 TUT502


class NT(NamedTuple):
    bar: int


class Specifier(Protocol):
    object_id: str


class FooEnum(Enum):
    foo = 1


@dataclass
class ExampleDataclass:
    a = 3  # noqa: TUT502
    x: int
    y: float
    z = field(default=4)  # noqa: TUT502

    Q = TypeVar("Q", bound="ExampleDataclass")

    def method(self) -> None:
        return None

    def __str__(self) -> str:
        return super().__str__()

    @classmethod
    def construct(cls) -> Self:
        raise NotImplementedError

    # other inline comment


@dataclasses.dataclass
class Example2:
    a = 3  # noqa: TUT502


@dataclass(frozen=True)
class Example3:
    a = 4  # noqa: TUT502
