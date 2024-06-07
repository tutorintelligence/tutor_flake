# type: ignore


from ast import TypeVar


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


# Test consecutive typing


async def a_c_1(a: int, b: int):  # noqa: TUT630
    ...


def c_1(a: int, b: int):  # noqa: TUT630
    ...


def c_2(a: "int", b: "int"):  # noqa: TUT630
    ...


def c_3(a: list[int], b: list[int]):  # noqa: TUT630
    ...


T = TypeVar("T")


def c_4(a: T, b: T):  # noqa: TUT630
    ...


def c_5(a: list[T], b: list[T]):  # noqa: TUT630
    ...


def c_6(a, b: int, c: int, d: float):  # noqa: TUT610 TUT630
    ...


def c_7(a: int, b: int, /, c: int, *, d: int, e: int):
    ...


def c_8(a: int, b: float, c: int, d: float):  # noqa: TUT610
    ...


def c_9(a: int, *b: int):
    ...
