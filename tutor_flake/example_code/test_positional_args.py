def func_1(a: int, b: int, c: int, d: int, e: int = 3) -> None:  # noqa: TUTOR610
    return None


def func_2(a: int, b: int, c: int, *, d: int) -> None:
    return None


def func_3(a: int, b: int, c: int, d: int = 3) -> None:
    return None


def func_4(a: int, b: int, c: int, /, d: int = 3) -> None:
    return None


def func_5(a: int, *b: int, c: int = 3) -> None:
    return None


class DummyClass:
    def func_1(self, a: int, b: int, c: int) -> None:
        pass

    def func_2(self, a: int, b: int, c: int, d: int) -> None:  # noqa: TUTOR610
        pass

    @classmethod
    def func_3(cls, a: int, b: int, c: int) -> None:
        pass

    @classmethod
    def func_4(cls, a: int, b: int, c: int, d: int) -> None:  # noqa: TUTOR610
        pass
