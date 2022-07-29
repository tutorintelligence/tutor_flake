import typing
from typing import Any, Generic, Mapping, TypeVar

T = TypeVar("T")
U = TypeVar("U")


class Foo(Generic[T]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()

    ...


class Bar(Generic[T, U]):
    ...


class Foo2(Foo):
    ...


if __name__ == "__main__":
    f_bad_1: Foo = Foo()  # noqa: TUTOR410
    f_bad_2: Foo[int] = Foo()  # noqa: TUTOR411
    f_bad_3: Foo[int] = Foo(1, 2, three=3)  # noqa: TUTOR411
    b_bad: Bar[int, typing.Sequence[float]] = Bar()  # noqa: TUTOR411

    f_good = Foo[int]()
    f_child: Foo[int] = Foo2()
    m: Mapping[str, int] = {}
