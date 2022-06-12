

async def example_async(x: int, y: float) -> bool:
    return True


async def example_async_2(x: int, y: float) -> bool:
    return await example_async(x, y)