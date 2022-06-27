import random
from typing import TYPE_CHECKING

t = 3


def func() -> int:
    print("hello")
    return 3


x = func()

func()  # noqa: TUTOR300


for z in [1, 2, 3]:
    random.random()  # noqa: TUTOR300

if TYPE_CHECKING:
    func()  # noqa: TUTOR300

if __name__ == "_main_":
    func()  # noqa: TUTOR300

if x == "__main__":
    func()  # noqa: TUTOR300

if __name__ == "__main__":
    func()
    z = 3
