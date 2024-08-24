from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Tuple

from typing_extensions import Self


class FooBar:
    @classmethod
    def bad_cls_construct(cls) -> "FooBar":  # noqa: TUT530
        raise NotImplementedError

    @staticmethod
    def bad_static_struct() -> "FooBar":  # noqa: TUT530
        raise NotImplementedError

    def bad_self_method(self) -> "FooBar":  # noqa: TUT530
        raise NotImplementedError

    def bad_complicated_return(self) -> Tuple[None, "FooBar"]:  # noqa: TUT530
        raise NotImplementedError

    @asynccontextmanager
    async def bad_complicated_return_2(  # noqa: TUT530 TUT210
        self,
    ) -> AsyncGenerator["FooBar", None]:
        yield self

    async def return_allowed_because_of_args(
        self, arg_1: List["FooBar"]
    ) -> List["FooBar"]:
        raise NotImplementedError

    def return_allowed_because_of_positional_only_arg(
        self,
        arg_1: "FooBar",
    ) -> "FooBar":
        raise NotImplementedError

    def return_allowed_because_of_keyword_only_arg(
        self, *, arg_1: "FooBar"
    ) -> "FooBar":
        raise NotImplementedError

    @classmethod
    def good_cls_construct(cls) -> Self:
        raise NotImplementedError
