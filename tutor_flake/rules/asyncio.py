import ast
from typing import Generator, Iterable, Optional

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


def is_node_async(node: ast.AST) -> bool:
    return isinstance(node, (ast.Await, ast.AsyncFor, ast.AsyncWith))


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
            or isinstance(first_line, ast.Return)
            or (
                isinstance(first_line, ast.Expr)
                and isinstance(val := first_line.value, ast.Constant)
                and (val.value == Ellipsis)
            )
        )

    @classmethod
    def has_async(cls, node: ast.AST) -> bool:
        if is_node_async(node):
            return True
        return any(
            (
                cls.has_async(child)
                for child in ast.iter_child_nodes(node)
                if not isinstance(child, ast.AsyncFunctionDef)
            )
        )


class HandlersAreSafeForCancelledErrors:
    @classmethod
    def check_except_handler(
        cls, node: ast.ExceptHandler
    ) -> Generator[Flake8Error, None, None]:
        if cls._is_type_cancelled_error(node.type):
            for error in cls._check_statements(node.body):
                yield error

    @classmethod
    def check_finally_body(cls, node: ast.Try) -> Generator[Flake8Error, None, None]:
        return cls._check_statements(node.finalbody)

    @classmethod
    def _is_type_cancelled_error(cls, type: Optional[ast.AST]) -> bool:
        if type is None or check_name_or_attribute(
            type, "CancelledError", "BaseException"
        ):
            return True
        elif isinstance(type, ast.Tuple):
            return any((cls._is_type_cancelled_error(elt) for elt in type.elts))
        return False

    @classmethod
    def _check_statements(
        cls, statements: Iterable[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        for statement in statements:
            if not isinstance(statement, ast.AsyncFunctionDef):
                for error in cls._check_statement(statement):
                    yield error

    @classmethod
    def _check_statement(cls, statement: ast.AST) -> Generator[Flake8Error, None, None]:
        if is_node_async(statement) and not cls._is_timeout_async_call(statement):
            yield Flake8Error.construct(
                statement,
                "220",
                "Unsafe asynchronous call in a try or finally block",
                cls,
            )
        for error in cls._check_statements(ast.iter_child_nodes(statement)):
            yield error

    @classmethod
    def _is_timeout_async_call(cls, node: ast.AST) -> bool:
        return (
            isinstance(node, ast.Await)
            and isinstance(value := node.value, ast.Call)
            and (
                cls._is_safe_wait(value)
                or check_name_or_attribute(value.func, "wait_for", "sleep")
            )
        )

    @staticmethod
    def _is_safe_wait(node: ast.Call) -> bool:
        return check_name_or_attribute(node.func, "wait") and any(
            kwarg.arg == "timeout" for kwarg in node.keywords
        )
