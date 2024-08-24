import ast
import itertools
from ast import Constant, expr, walk
from typing import Generator, List

from tutor_flake.common import Flake8Error


class ConstructorIsWellTyped:
    @classmethod
    def check(
        cls, func: ast.FunctionDef | ast.AsyncFunctionDef, parents: List[ast.AST]
    ) -> Generator[Flake8Error, None, None]:
        class_definition = next(
            (
                parent
                for parent in reversed(parents)
                if isinstance(parent, ast.ClassDef)
            ),
            None,
        )
        if class_definition is None:
            return
        class_name = class_definition.name
        for func_arg in itertools.chain(
            func.args.posonlyargs, func.args.args, func.args.kwonlyargs
        ):
            if (
                annotation := func_arg.annotation
            ) is not None and does_type_annotation_include_type(annotation, class_name):
                # we allow the return type if an argument includes the class name
                return
        if (
            func_return := func.returns
        ) is not None and does_type_annotation_include_type(func_return, class_name):
            yield Flake8Error.construct(
                func,
                530,
                f"Funciton `{func.name}`'s return value includes the class type: `{class_name}`."
                " Likely you want to return the Self type imported from `typing` or `typing_extensions`"
                " as child types likely should return their own type.",
                cls,
            )


def does_type_annotation_include_type(annotation: expr, check_type: str) -> bool:
    for child_node in walk(annotation):
        if isinstance(child_node, Constant) and child_node.value == check_type:
            return True
    return False
