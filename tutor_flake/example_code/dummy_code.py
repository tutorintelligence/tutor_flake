import asyncio


def hello(x: int) -> str:
    return str(x)


async def example_async(x: int, y: float) -> bool:
    return True


def task_creation() -> None:
    x = asyncio.create_task(example_async(3, 4))
    print(x)
