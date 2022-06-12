import asyncio
from dataclasses import dataclass


def hello(x: int) -> str:
    return str(x)


async def example_async(x: int, y: float) -> bool:
    return True


def task_creation() -> None:
    x = asyncio.create_task(example_async(3, 4))
    print(x)


@dataclass
class ExampleDataclass:
    a = 3  # noqa: TUTOR100
    x: int
    y: float

    def method(self) -> None:
        return None

    def __str__(self) -> str:
        return super().__str__()

    @classmethod
    def construct(cls) -> "ExampleDataclass":
        raise NotImplementedError

    # other inline comment
