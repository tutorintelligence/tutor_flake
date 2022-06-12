import asyncio
from asyncio import create_task


def main() -> None:
    _ = asyncio.create_task(foo(), name="1")
    _ = create_task(foo(), name="1")
    _ = asyncio.create_task(foo())  # noqa: TUTOR200
    _ = create_task(foo())  # noqa: TUTOR200


async def foo() -> float:
    return 3
