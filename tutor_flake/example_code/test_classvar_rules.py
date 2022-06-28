class DummyClass:

    a: int = 4
    b: float
    c = "abc"
    d = bool

    def __init__(self, value: float) -> None:
        self.a = 3  # noqa: TUTOR500
        if 3 - 2 == 1:
            self.b = value  # noqa: TUTOR500
        self.b += 1.3  # noqa: TUTOR500
        self.c = str(value)  # noqa: TUTOR500
        d = 4
        print(d)
        self.x = value

    def __repr__(self) -> str:
        return f"{self.a} {self.b} {self.x}"

    @classmethod
    def override(cls, new_c: str) -> None:
        cls.c = new_c

    def instance_override(self, new_c: str) -> None:
        # we allow this, but is still bad
        self.c = new_c

    e: bool  # noqa: TUTOR501
    f = 3  # noqa: TUTOR501
