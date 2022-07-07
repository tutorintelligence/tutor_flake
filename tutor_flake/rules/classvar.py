import ast
from typing import Generator, List, Optional

from tutor_flake.common import (
    Flake8Error,
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


def is_named_tuple(node: ast.ClassDef) -> bool:
    return any(check_name_or_attribute(base, "NamedTuple") for base in node.bases)


class ClassvarCheck:
    # confirms
    @classmethod
    def check(cls, node: ast.ClassDef) -> Generator[Flake8Error, None, None]:
        class_variables: List[str] = []
        init_function: Optional[ast.FunctionDef] = None
        function_seen = False
        for child in node.body:
            if isinstance(child, (ast.AnnAssign, ast.Assign)):
                for target in get_targets(child):
                    target_id: str = target.id  # type: ignore
                    class_variables.append(target_id)
                    if function_seen:
                        yield Flake8Error.construct(
                            child,
                            "501",
                            f"Class variable `{target_id}` instantiated after methods",
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

                    elif not is_dataclass(node) and not is_named_tuple(node):
                        if (
                            not isinstance(
                                annotation := child.annotation, ast.Subscript
                            )
                            or not isinstance(val := annotation.value, ast.Name)
                            or not check_name_or_attribute(val, "ClassVar")
                        ):  # TODO
                            yield Flake8Error.construct(
                                child,
                                "503",
                                "Class variable must be type annotated with `ClassVar`",
                                cls,
                            )

            elif isinstance(child, ast.FunctionDef):
                function_seen = True
                if child.name == "__init__":
                    init_function = child

        if init_function is not None:
            for module in ast.walk(init_function):
                if isinstance(module, (ast.AnnAssign, ast.AugAssign, ast.Assign)):
                    for target in get_targets(module):
                        if (
                            isinstance(target, ast.Attribute)
                            and check_name_or_attribute(target.value, "self")
                            and target.attr in class_variables
                        ):
                            yield Flake8Error.construct(
                                target,
                                "500",
                                f"Instance variable `{target.attr}` overlaps with a class variable",
                                cls,
                            )
