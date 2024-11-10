import ast
from typing import Generator

from tutor_flake.common import (
    Flake8Error,
    check_annotation,
    check_is_subclass,
    get_targets,
    is_dataclass,
    is_type_var,
)


class ClassvarCheck:
    @classmethod
    def check(cls, node: ast.ClassDef) -> Generator[Flake8Error, None, None]:
        function_seen = False
        for child in node.body:
            if isinstance(child, (ast.AnnAssign, ast.Assign)):
                for target in get_targets(child):
                    if function_seen:
                        target_id = getattr(target, "id", None)
                        yield Flake8Error.construct(
                            child,
                            501,
                            (
                                f"Class variable `{target_id}` instantiated after methods"
                                if target_id is not None
                                else "Class variable instantiated after methods"
                            ),
                            cls,
                        )
                if not cls.is_class_exempt_from_type_annotations(
                    node
                ) and not is_type_var(child.value):
                    if isinstance(child, ast.Assign):
                        yield Flake8Error.construct(
                            child,
                            502,
                            "Class variable must be type annotated",
                            cls,
                        )

                    elif not cls.is_class_exempt_from_class_var_type_annotations(
                        node
                    ) and not (
                        check_annotation(child, "ClassVar")
                        or check_annotation(child, "Final")
                    ):
                        yield Flake8Error.construct(
                            child,
                            503,
                            "Class variable must be type annotated with `ClassVar` or `Final`",
                            cls,
                        )

            elif isinstance(child, ast.FunctionDef):
                function_seen = True

    @classmethod
    def is_class_exempt_from_type_annotations(cls, node: ast.ClassDef) -> bool:
        return check_is_subclass(node, "Enum", "IntEnum")

    @classmethod
    def is_class_exempt_from_class_var_type_annotations(
        cls, node: ast.ClassDef
    ) -> bool:
        return is_dataclass(node) or check_is_subclass(  # noqa: TUT620
            node,
            "NamedTuple",
            "Protocol",
            "Enum",
            "IntEnum",
            "TypedDict",
            "BaseModel",
            "NumpyModel",
        )
