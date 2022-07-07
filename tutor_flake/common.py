import ast
from typing import List, NamedTuple, Type, Union


class Flake8Error(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type  # currently unused but required

    @classmethod
    def construct(  # noqa: TUTOR610
        cls,
        node: ast.AST,
        code: str,
        description: str,
        rule_cls: type,
    ) -> "Flake8Error":
        return Flake8Error(
            node.lineno, node.col_offset, f"TUTOR{code} {description}", rule_cls
        )


def check_name_or_attribute(node: ast.AST, *name_or_attr: str) -> bool:
    return (isinstance(node, ast.Name) and node.id in name_or_attr) or (
        isinstance(node, ast.Attribute) and node.attr in name_or_attr
    )


def has_keyword(call: ast.Call, keyword: str) -> bool:
    return any(kw.arg == keyword for kw in call.keywords)


def get_targets(
    assignment: Union[ast.AnnAssign, ast.Assign, ast.AugAssign]
) -> List[ast.expr]:
    if isinstance(assignment, ast.Assign):
        return assignment.targets
    return [assignment.target]


def is_type_var(node: ast.AST) -> bool:
    return isinstance(node, ast.Call) and check_name_or_attribute(node.func, "TypeVar")


def check_any_parent(parents: List[ast.AST], *types: Type[ast.AST]) -> bool:
    return any(isinstance(node, types) for node in parents)
