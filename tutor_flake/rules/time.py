import ast
from typing import Generator

from tutor_flake.common import Flake8Error


class NoTimeDotTime:
    @classmethod
    def check(cls, attr: ast.Attribute) -> Generator[Flake8Error, None, None]:
        if (
            attr.attr == "time"
            and isinstance(attr.value, ast.Name)
            and attr.value.id == "time"
        ):
            yield Flake8Error.construct(
                attr,
                "800",
                "time.time() can jump and is not monotonic: are you sure it is what you want?",
                cls,
            )


class NoFromTimeTimeImports:
    @classmethod
    def check(cls, node: ast.ImportFrom) -> Generator[Flake8Error, None, None]:
        if node.module == "time" and any([name.name == "time" for name in node.names]):
            yield Flake8Error.construct(
                node,
                "810",
                "time.time() can jump and is not monotonic: are you sure it is what you want?",
                cls,
            )
