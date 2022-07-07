class Foo:
    def __init__(self) -> None:
        super(Foo, self).__init__()  # noqa: TUTOR510

    def __str__(self) -> str:
        return super().__str__()


x = super(Foo, Foo())
