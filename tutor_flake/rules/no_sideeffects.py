import ast
from typing import List, Union

from tutor_flake.common import Flake8Error


class NoSideeffects:
    @classmethod
    def check(cls, node: ast.Module) -> List[Flake8Error]:
        return cls.recursive_check(node)

    @classmethod
    def recursive_check(
        cls, node: Union[ast.Module, ast.For, ast.While, ast.Try, ast.If]
    ) -> List[Flake8Error]:
        errors: List[Flake8Error] = []
        for child in node.body:
            if isinstance(child, ast.Expr) and not isinstance(
                child.value, ast.Constant
            ):
                errors.append(
                    Flake8Error.construct(
                        child,
                        300,
                        "found an expression in the main module body",
                        cls,
                    )
                )
            if isinstance(child, (ast.For, ast.While, ast.Try,)) or (
                isinstance(child, ast.If)
                and not cls.check_if_name_is_main_conditional(child)
            ):
                errors += cls.recursive_check(child)
        return errors

    @classmethod
    def check_if_name_is_main_conditional(cls, node: ast.If) -> bool:
        return (
            isinstance(comp := node.test, ast.Compare)
            and isinstance(left := comp.left, ast.Name)
            and isinstance(left.ctx, ast.Load)
            and left.id == "__name__"
            and len(ops := comp.ops) == 1
            and isinstance(ops[0], ast.Eq)
            and len(comp.comparators) == 1
            and isinstance(right := comp.comparators[0], ast.Constant)
            and right.value == "__main__"
        )
