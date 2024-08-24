import ast
from typing import List, NamedTuple, Optional, Type, Union

from typing_extensions import Self


class Flake8Error(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type  # currently unused but required

    @classmethod
    def construct(  # noqa: TUT610
        cls,
        node: ast.AST,
        code: int,
        description: str,
        rule_cls: type,
    ) -> Self:
        return cls(
            node.lineno,  # type: ignore
            node.col_offset,  # type: ignore
            f"TUT{code} {description}",
            rule_cls,
        )


def recursive_check_name_or_attribute(node: ast.AST, *name_or_attrs: str) -> bool:
    if isinstance(node, ast.Attribute):
        return check_attribute(
            node, *name_or_attrs
        ) or recursive_check_name_or_attribute(node.value, *name_or_attrs)
    return check_name(node, *name_or_attrs)


def check_name_or_attribute(node: ast.AST, *name_or_attrs: str) -> bool:
    return check_name(node, *name_or_attrs) or check_attribute(node, *name_or_attrs)


def check_name(node: ast.AST, *names: str) -> bool:
    return isinstance(node, ast.Name) and node.id in names


def check_attribute(node: ast.AST, *attrs: str) -> bool:
    return isinstance(node, ast.Attribute) and node.attr in attrs


def has_keyword(call: ast.Call, keyword: str) -> bool:
    return any(kw.arg == keyword for kw in call.keywords)


def get_targets(
    assignment: Union[ast.AnnAssign, ast.Assign, ast.AugAssign]
) -> List[ast.expr]:
    if isinstance(assignment, ast.Assign):
        return assignment.targets
    return [assignment.target]


def is_type_var(node: Optional[ast.AST]) -> bool:
    return (
        node is not None
        and isinstance(node, ast.Call)
        and check_name_or_attribute(node.func, "TypeVar")
    )


def check_any_parent(parents: List[ast.AST], *types: Type[ast.AST]) -> bool:
    return any(isinstance(node, types) for node in parents)


def check_annotation(assignment: ast.AnnAssign, name: str) -> bool:
    if isinstance(annotation := assignment.annotation, ast.Name):
        return check_name_or_attribute(annotation, name)
    elif isinstance(annotation, ast.Subscript):
        return check_name_or_attribute(annotation.value, name)
    return False


def check_is_subclass(node: ast.ClassDef, *name_or_attr: str) -> bool:
    return any(check_name_or_attribute(base, *name_or_attr) for base in node.bases)


def check_name_equality(name: ast.Name, other: ast.Name, /) -> bool:
    return name.id == other.id and name.ctx == other.ctx


def is_dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        if check_name_or_attribute(decorator, "dataclass") or (
            isinstance(decorator, ast.Call)
            and check_name_or_attribute(decorator.func, "dataclass")
        ):
            return True
    return False
