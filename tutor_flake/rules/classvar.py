import ast
from typing import Generator

from tutor_flake.common import (
    Flake8Error,
    check_annotation,
    check_is_subclass,
    check_name_or_attribute,
    get_targets,
    is_type_var,
)


def is_dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        if check_name_or_attribute(decorator, "dataclass") or (
            isinstance(decorator, ast.Call)
            and check_name_or_attribute(decorator.func, "dataclass")
        ):
            return True
    return False


class ClassvarCheck:
    @classmethod
    def check(cls, node: ast.ClassDef) -> Generator[Flake8Error, None, None]:
        function_seen = False
        for child in node.body:
            if isinstance(child, (ast.AnnAssign, ast.Assign)):
                for target in get_targets(child):
                    if function_seen:
                        yield Flake8Error.construct(
                            child,
                            "501",
                            f"Class variable `{target.id}` instantiated after methods",  # type: ignore
                            cls,
                        )
                if not is_type_var(child.value):
                    if isinstance(child, ast.Assign):
                        yield Flake8Error.construct(
                            child,
                            "502",
                            "Class variable must be type annotated",
                            cls,
                        )

                    elif not cls.is_excepted_class(node) and not check_annotation(
                        child, "ClassVar"
                    ):
                        yield Flake8Error.construct(
                            child,
                            "503",
                            "Class variable must be type annotated with `ClassVar`",
                            cls,
                        )

            elif isinstance(child, ast.FunctionDef):
                function_seen = True

    @classmethod
    def is_excepted_class(cls, node: ast.ClassDef) -> bool:
        return is_dataclass(node) or check_is_subclass(node, "NamedTuple", "Protocol")
