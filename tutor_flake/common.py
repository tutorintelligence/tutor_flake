import ast
from typing import NamedTuple


class Flake8Error(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type  # currently unused but required

    @classmethod
    def construct(
        cls, node: ast.AST, code: str, description: str, rule_cls: type
    ) -> "Flake8Error":
        return Flake8Error(
            node.lineno, node.col_offset, f"TUTOR{code} {description}", rule_cls
        )


def check_name_or_attribute(node: ast.AST, *name_or_attr: str) -> bool:
    return (isinstance(node, ast.Name) and node.id in name_or_attr) or (
        isinstance(node, ast.Attribute) and node.attr in name_or_attr
    )
