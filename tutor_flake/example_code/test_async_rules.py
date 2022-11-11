import asyncio
from asyncio import CancelledError, create_task
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


async def try_catch_with_unsafe_async_handlers() -> Any:
    try:
        await foo()
    except (CancelledError, AssertionError):
        await foo()  # noqa: TUTOR220
        await asyncio.wait(foo())  # noqa: TUTOR220
        for _ in [1, 2, 3]:
            await foo()  # noqa: TUTOR220
    except (asyncio.CancelledError):
        async for x in foo():  # noqa: TUTOR220
            return x
    except (asyncio.exceptions.CancelledError):
        async with foo() as x:  # noqa: TUTOR220
            return x
    except BaseException:
        await foo()  # noqa: TUTOR220
    except:  # noqa: E722
        await foo()  # noqa: TUTOR220
    finally:
        await foo()  # noqa: TUTOR220


async def try_catch_with_safe_async_handlers() -> Any:
    try:
        await foo()
    except (CancelledError, AssertionError):
        await asyncio.sleep(3)
        await asyncio.wait(foo(), timeout=3)
        await asyncio.wait_for(foo(), 7)
        await asyncio.wait_for(foo(), timeout=7)
    finally:
        await asyncio.wait(foo(), timeout=3)


async def catch_with_sync_exception_and_finally() -> Any:
    try:
        await foo()
    except RuntimeError:

        async def bar() -> None:
            await foo()

    finally:

        async def bar() -> None:
            await foo()

        print(3 + 4)
