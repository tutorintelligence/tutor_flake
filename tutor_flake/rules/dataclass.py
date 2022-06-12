import ast
from typing import Generator

from tutor_flake.common import Flake8Error, check_name_or_attribute


class DataclassMissingAnnotations:
    @classmethod
    def check(cls, node: ast.ClassDef) -> Generator[Flake8Error, None, None]:
        if is_dataclass(node):
            for child in node.body:
                if isinstance(child, ast.Assign) and child.type_comment is None:
                    yield Flake8Error.construct(
                        child,
                        "100",
                        "Dataclass missing annotation for a class variable",
                        cls,
                    )


class DataclassRenamed:
    @classmethod
    def check(cls, node: ast.ImportFrom) -> Generator[Flake8Error, None, None]:
        if node.module == "dataclasses":
            for name in node.names:
                if name.name == "dataclass" and name.asname is not None:
                    yield Flake8Error.construct(
                        node, "101", "Dataclass renamed on import", cls
                    )


def is_dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        if check_name_or_attribute(decorator, "dataclass"):
            return True
    return False
