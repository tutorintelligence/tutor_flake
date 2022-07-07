cd = 100

u = True
v = 10
w = "abcd"
x = "abc{d"
y = "ab}c{d"
z = "ab{cd}"  # noqa: TUTOR400
z2 = f"ab{cd}"

multiline = """
{} hello
"""


def func(t: str) -> str:
    w = "abcd"
    x = "abc{d"
    y = "ab}c{d"
    z = "ab{cd}"  # noqa: TUTOR400
    z2 = f"ab{cd}"
    return w + x + y + z + z2


a = func("{abcd}")  # noqa: TUTOR400
b = func(f"ab{cd = }")
