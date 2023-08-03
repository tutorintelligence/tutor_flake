import ast
from typing import Generator, Iterable, Optional

from tutor_flake.common import (
    Flake8Error,
    check_attribute,
    check_name_or_attribute,
    has_keyword,
)


class CreateTaskRequireName:
    @classmethod
    def check(cls, node: ast.Call) -> Generator[Flake8Error, None, None]:
        if check_name_or_attribute(node.func, "create_task") and not has_keyword(
            node, "name"
        ):
            yield Flake8Error.construct(
                node, "200", "create_task function missing `name` keyword argument", cls
            )


class CreateTaskIsAssigned:
    @classmethod
    def check(cls, node: ast.Expr) -> Generator[Flake8Error, None, None]:
        if isinstance(node.value, ast.Call) and check_name_or_attribute(
            node.value.func, "create_task"
        ):
            yield Flake8Error.construct(
                node,
                "201",
                "create_task function not assigned to a value or await-ed",
                cls,
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


class CancelPassedMessage:
    @classmethod
    def check(cls, invocation: ast.Call) -> Generator[Flake8Error, None, None]:
        if check_attribute(invocation.func, "cancel"):
            args = invocation.args
            kwargs = invocation.keywords
            total_arg_num = len(args) + len(kwargs)
            if total_arg_num > 1:
                # too many arguments, does not match the spec of asyncio.cancel
                return
            elif total_arg_num == 0:
                yield Flake8Error.construct(
                    invocation,
                    "230",
                    "A call presumed to be `cancel` on an asyncio.Task was made without providing a message",
                    cls,
                )
            elif len(args) == 1 and cls._is_parameter_None_literal(args[0]):
                yield Flake8Error.construct(
                    invocation,
                    "230",
                    "A call presumed to be `cancel` on an asyncio.Task was made with a `None` messsage",
                    cls,
                )
            elif (
                len(kwargs) == 1
                and (kwarg := kwargs[0]).arg == "msg"
                and cls._is_parameter_None_literal(kwarg.value)
            ):
                yield Flake8Error.construct(
                    invocation,
                    "230",
                    "A call presumed to be `cancel` on an asyncio.Task was made with a `None` messsage",
                    cls,
                )

    @classmethod
    def _is_parameter_None_literal(cls, parameter: ast.expr) -> bool:
        return isinstance(parameter, ast.Constant) and parameter.value is None
