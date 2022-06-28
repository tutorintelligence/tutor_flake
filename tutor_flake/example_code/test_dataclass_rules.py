"""
isort:skip_file
"""
import dataclasses
from dataclasses import dataclass
from dataclasses import dataclass as dc, field  # noqa: TUTOR101


@dataclass
class ExampleDataclass:
    a = 3  # noqa: TUTOR100
    x: int
    y: float
    z = field(default=4)  # noqa: TUTOR100

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
    a = 3  # noqa: TUTOR100


@dataclass(frozen=True)
class Example3:
    a = 4  # noqa: TUTOR100


@dc
class Example4:
    a = 3
