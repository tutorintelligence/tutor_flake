import typing
from dataclasses import dataclass
from queue import Queue
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


@dataclass
class Baz:
    foo: Foo = Foo()  # should be allowed


if __name__ == "__main__":
    f_bad_1: Foo = Foo()  # noqa: TUT410
    f_bad_2: Foo[int] = Foo()  # noqa: TUT411
    f_bad_3: Foo[int] = Foo(1, 2, three=3)  # noqa: TUT411
    b_bad: Bar[int, typing.Sequence[float]] = Bar()  # noqa: TUT411

    q: Queue[int] = Queue()
    f_good = Foo[int]()
    f_child: Foo[int] = Foo2()
    m: Mapping[str, int] = {}
