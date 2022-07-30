import ast
from typing import Generator, Optional

from tutor_flake.common import Flake8Error, check_name_equality, is_dataclass


class CompactGeneric:
    @classmethod
    def check(
        cls, node: ast.AnnAssign, parent: Optional[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        if not isinstance(parent, ast.ClassDef) or not is_dataclass(parent):
            if (
                isinstance(call := node.value, ast.Call)
                and isinstance(func_call := call.func, ast.Name)
                and not cls.is_name_excepted(func_call)
            ):
                if isinstance(annotation := node.annotation, ast.Name):
                    if check_name_equality(annotation, func_call):
                        yield Flake8Error.construct(
                            node, "410", "Redundant typing", cls
                        )
                elif isinstance(annotation, ast.Subscript) and isinstance(
                    annotation_name := annotation.value, ast.Name
                ):
                    if check_name_equality(annotation_name, func_call):
                        yield Flake8Error.construct(
                            node,
                            "411",
                            "Redundant typing - move generic arguments to the function call itself",
                            cls,
                        )

    @staticmethod
    def is_name_excepted(name: ast.Name) -> bool:
        return name.id == "Queue"
