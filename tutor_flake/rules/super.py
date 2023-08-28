import ast
from typing import Generator, List

from tutor_flake.common import Flake8Error, check_any_parent, check_name_or_attribute


def is_call_super(call: ast.Call) -> bool:
    return isinstance(name := call.func, ast.Name) and name.id == "super"


class NoTwoArgumentSuper:
    @classmethod
    def check(
        cls, call: ast.Call, parents: List[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        if (
            is_call_super(call)
            and len(call.args) == 2
            and check_any_parent(parents, ast.ClassDef)
        ):
            yield Flake8Error.construct(
                call, "510", "Do not use two argument super within a class", cls
            )


def get_non_generic_bases(class_def: ast.ClassDef) -> List[ast.expr]:
    return [
        base
        for base in class_def.bases
        if not (
            isinstance(base, ast.Subscript)
            and check_name_or_attribute(base.value, "Generic")
        )
    ]


class ChildClassCallsSuperMethods:
    @classmethod
    def check(
        cls, func: ast.FunctionDef, parents: List[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        yield from cls.test_method_calls_parent_method(func, parents, "__init__")
        yield from cls.test_method_calls_parent_method(func, parents, "__post_init__")

    @classmethod
    def test_method_calls_parent_method(
        cls, func: ast.FunctionDef, parents: List[ast.AST], function_name: str
    ) -> Generator[Flake8Error, None, None]:
        if func.name == function_name:
            class_definition = next(
                (
                    parent
                    for parent in reversed(parents)
                    if isinstance(parent, ast.ClassDef)
                ),
                None,
            )
            if (
                class_definition is not None
                and len(get_non_generic_bases(class_definition)) > 0
            ):
                for statement in func.body:
                    if (
                        isinstance(statement, ast.Expr)
                        and isinstance(call := statement.value, ast.Call)
                        and isinstance(attr := call.func, ast.Attribute)
                        and attr.attr == function_name
                        and isinstance(attr.value, ast.Call)
                        and is_call_super(attr.value)
                    ):
                        # found call
                        break
                else:
                    yield Flake8Error.construct(
                        func,
                        "511",
                        f"{function_name} function did not call super().{function_name}",
                        cls,
                    )
