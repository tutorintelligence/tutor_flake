def func_1(a: int, b: int, c: int, d: int, e: int = 3) -> int:  # noqa: TUTOR610
    pass


def func_2(a: int, b: int, c: int, *, d: int) -> int:
    pass


def func_3(a: int, b: int, c: int, d: int = 3) -> int:
    pass


def func_4(a: int, b: int, c: int, /, d: int = 3) -> int:
    pass


def func_5(a: int, *b: int, c: int = 3) -> int:
    pass


class DummyClass:
    def func_1(self, a: int, b: int, c: int) -> int:
        pass

    def func_2(self, a: int, b: int, c: int, d: int) -> int:  # noqa: TUTOR610
        pass

    @classmethod
    def func_3(cls, a: int, b: int, c: int) -> int:
        pass

    @classmethod
    def func_4(cls, a: int, b: int, c: int, d: int) -> int:  # noqa: TUTOR610
        pass


a = func_1(0, 1, 2, 3, 4)  # noqa: TUTOR620
b = func_1(0, 1, 2, 3, e=5)
d = func_5(0)
e = func_5(0, 1, 2, 3, c=4)
f = func_5(0, 1, 2, 3, 4)  # noqa: TUTOR620
