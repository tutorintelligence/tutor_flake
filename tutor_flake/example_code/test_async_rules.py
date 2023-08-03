import asyncio
from asyncio import CancelledError, create_task
from typing import Any


def foo() -> Any:
    ...


def main() -> None:
    _ = asyncio.create_task(foo(), name="1")
    _ = create_task(foo(), name="1")
    _ = asyncio.create_task(foo())  # noqa: TUT200
    _ = create_task(foo())  # noqa: TUT200


async def test_201() -> asyncio.Task:
    await create_task(foo(), name="1")
    await (create_task(foo(), name="1"))
    create_task(foo(), name="1")  # noqa: TUT201
    (create_task(foo(), name="1"))  # noqa: TUT201
    return create_task(foo(), name="1")


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


async def no_await() -> Any:  # noqa: TUT210
    x = 4
    y = x + 3

    async def func() -> None:
        await foo()

    return str(y)


async def try_catch_with_unsafe_async_handlers() -> Any:
    try:
        await foo()
    except (CancelledError, AssertionError):
        await foo()  # noqa: TUT220
        await asyncio.wait(foo())  # noqa: TUT220
        for _ in [1, 2, 3]:
            await foo()  # noqa: TUT220
    except (asyncio.CancelledError):
        async for x in foo():  # noqa: TUT220
            return x
    except (asyncio.exceptions.CancelledError):
        async with foo() as x:  # noqa: TUT220
            return x
    except BaseException:
        await foo()  # noqa: TUT220
    except:  # noqa: E722
        await foo()  # noqa: TUT220
    finally:
        await foo()  # noqa: TUT220


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


async def try_catch_with_sync_exception_and_finally() -> Any:
    try:
        await foo()
    except CancelledError:

        async def bar() -> None:
            await foo()

    finally:

        async def bar() -> None:
            await foo()

        print(3 + 4)


async def try_catch_with_async_handlers_in_safe_exceptions() -> Any:
    try:
        await foo()
    except RuntimeError:
        await foo()
    except (AssertionError, KeyError):
        await foo()
    except Exception:
        await foo()


def cancel() -> None:
    ...


def test_cancel_rules() -> None:
    cancel()  # does not error because not an attribute

    Foo = foo()

    # standard illegal calls
    Foo.cancel()  # noqa: TUT230
    Foo.cancel(None)  # noqa: TUT230
    Foo.cancel(msg=None)  # noqa: TUT230

    # standard legal calls
    Foo.cancel(msg="")
    Foo.cancel("")

    # calls which do not match the spec of cancel
    Foo.cancel(bar=3)
    Foo.cancel(bar=3, baz=1)
    Foo.cancel(bar=3, msg=None)

    Foo.cancel(3, msg=None)
    Foo.cancel(3, bar=None)

    Foo.cancel(3, 4)
    Foo.cancel(None, None)

    cancel()
