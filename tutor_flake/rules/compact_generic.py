import ast
from typing import Generator

from tutor_flake.common import Flake8Error, check_name_equality


class CompactGeneric:
    @classmethod
    def check(cls, node: ast.AnnAssign) -> Generator[Flake8Error, None, None]:
        if isinstance(call := node.value, ast.Call):
            func_call = call.func
            if isinstance(annotation := node.annotation, ast.Name):
                if check_name_equality(annotation, func_call):
                    yield Flake8Error.construct(node, "410", "Redundant typing", cls)
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
