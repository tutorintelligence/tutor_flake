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


class AsyncFunctionsAreAsynchronous:
    @classmethod
    def check(cls, node: ast.AsyncFunctionDef) -> Generator[Flake8Error, None, None]:
        if not cls.is_basic(node) and not cls.has_async(node):
            yield Flake8Error.construct(
                node, "210", "Function does not need to be asynchronous", cls
            )

    @classmethod
    def is_basic(cls, node: ast.AsyncFunctionDef) -> bool:
        first_line = node.body[0]
        return (
            isinstance(first_line, ast.Raise)
            or isinstance(first_line, ast.Pass)
            or (
                isinstance(first_line, ast.Expr)
                and isinstance(val := first_line.value, ast.Constant)
                and (val.value == Ellipsis)
            )
        )

    @classmethod
    def has_async(cls, node: ast.AST) -> bool:
        if isinstance(node, (ast.Await, ast.AsyncFor, ast.AsyncWith)):
            return True
        return any(
            (
                cls.has_async(child)
                for child in ast.iter_child_nodes(node)
                if not isinstance(child, ast.AsyncFunctionDef)
            )
        )
