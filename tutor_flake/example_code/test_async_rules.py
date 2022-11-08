import asyncio
from asyncio import create_task
from typing import Any


def foo() -> Any:
    ...


def main() -> None:
    _ = asyncio.create_task(foo(), name="1")
    _ = create_task(foo(), name="1")
    _ = asyncio.create_task(foo())  # noqa: TUTOR200
    _ = create_task(foo())  # noqa: TUTOR200


async def use_async_context_manager() -> Any:
    async with foo() as x:
        return x


async def use_async_iterator() -> Any:
    async for x in foo():
        return x


async def use_normal_await() -> Any:
    for _ in [1, 2, 3]:
        return await foo()


async def raise_error() -> Any:
    raise NotImplementedError()


async def use_pass() -> Any:
    pass


async def use_dot_dot_dot() -> Any:
    ...


async def immediate_return() -> Any:
    return 0


async def no_await() -> Any:  # noqa: TUTOR210
    x = 4
    y = x + 3

    async def func() -> None:
        await foo()

    return str(y)
