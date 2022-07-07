import ast
from typing import Generator, List

from tutor_flake.common import Flake8Error, check_any_parent


class NoTwoArgumentSuper:
    @classmethod
    def check(
        cls, call: ast.Call, parents: List[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        if (
            isinstance(name := call.func, ast.Name)
            and name.id == "super"
            and len(call.args) == 2
            and check_any_parent(parents, ast.ClassDef)
        ):
            yield Flake8Error.construct(
                call, "510", "Do not use two argument super within a class", cls
            )
