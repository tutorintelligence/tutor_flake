import dataclasses
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, List, NamedTuple, Protocol, TypeVar


class DummyClass:

    a: int = 4  # noqa: TUTOR503
    b: float  # noqa: TUTOR503
    c = "abc"  # noqa: TUTOR502
    d = bool  # noqa: TUTOR502
    e: "str" = "abc"  # noqa: TUTOR503
    f: ClassVar
    g: ClassVar[bool] = False
    h: ClassVar[List[bool]]

    def __init__(self, value: float) -> None:
        self.a = 3  # noqa: TUTOR500
        if 3 - 2 == 1:
            self.b = value  # noqa: TUTOR500
        self.b += 1.3  # noqa: TUTOR500
        self.c = str(value)  # noqa: TUTOR500
        d = 4
        print(d)
        self.x = value

    def __repr__(self) -> str:
        return f"{self.a} {self.b} {self.x}"

    @classmethod
    def override(cls, new_c: str) -> None:
        cls.c = new_c

    def instance_override(self, new_c: str) -> None:
        # we allow this, but is still bad
        self.c = new_c

    i: ClassVar[bool]  # noqa: TUTOR501
    j = 3  # noqa: TUTOR501 TUTOR502


class NT(NamedTuple):
    bar: int


class Specifier(Protocol):
    object_id: str


class FooEnum(Enum):
    foo: int


@dataclass
class ExampleDataclass:
    a = 3  # noqa: TUTOR502
    x: int
    y: float
    z = field(default=4)  # noqa: TUTOR502

    Q = TypeVar("Q", bound="ExampleDataclass")

    def method(self) -> None:
        return None

    def __str__(self) -> str:
        return super().__str__()

    @classmethod
    def construct(cls) -> "ExampleDataclass":
        raise NotImplementedError

    # other inline comment


@dataclasses.dataclass
class Example2:
    a = 3  # noqa: TUTOR502


@dataclass(frozen=True)
class Example3:
    a = 4  # noqa: TUTOR502
