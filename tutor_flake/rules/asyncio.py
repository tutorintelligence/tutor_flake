import ast
from typing import Generator

from tutor_flake.common import Flake8Error, check_name_or_attribute, has_keyword


class CreateTaskRequireName:
    @classmethod
    def check(cls, node: ast.Call) -> Generator[Flake8Error, None, None]:
        if check_name_or_attribute(node.func, "create_task") and not has_keyword(
            node, "name"
        ):
            yield Flake8Error.construct(
                node, "200", "create_task function missing `name` keyword argument", cls
            )
