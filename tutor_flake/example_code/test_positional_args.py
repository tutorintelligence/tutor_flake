# type: ignore


def func_1(a, b, c, d, e=3) -> int:  # noqa: TUT610
    pass


async def afunc_1(a, b, c, d, e=3) -> int:  # noqa: TUT610
    pass


def func_2(a, b, c, *, d) -> int:
    pass


def func_3(a, b, c, d=3) -> int:
    pass


def func_4(a, b, c, /, d=3) -> int:
    pass


def func_5(a, *b, c=3) -> int:
    pass


class DummyClass:
    def func_1(self, a, b, c) -> int:
        pass

    def func_2(self, a, b, c, d) -> int:  # noqa: TUT610
        pass

    @classmethod
    def func_3(cls, a, b, c) -> int:
        pass

    @classmethod
    def func_4(cls, a, b, c, d) -> int:  # noqa: TUT610
        pass


a = func_1(0, 1, 2, 3, 4)  # noqa: TUT620
b = func_1(0, 1, 2, 3, e=5)
d = func_5(0)
e = func_5(0, 1, 2, 3, c=4)
f = func_5(0, 1, 2, 3, 4)  # noqa: TUT620


async def g() -> None:
    await afunc_1(0, 1, 2, 3, 4)  # noqa: TUT620
