import ast
import itertools
from typing import Generator, Optional

from tutor_flake.common import Flake8Error


class MaxPostionalArgsInFunctionDef:
    @classmethod
    def check(
        cls, func: ast.FunctionDef | ast.AsyncFunctionDef, max_positional: int
    ) -> Generator[Flake8Error, None, None]:
        num_pos_only = len(func.args.posonlyargs)
        num_args = len(func.args.args)
        num_defaults = len(func.args.defaults)
        self_or_class_exception = 1 if cls.class_or_self(cls.first_arg(func)) else 0
        num_positional = (
            num_pos_only + num_args - num_defaults - self_or_class_exception
        )
        if num_positional > max_positional:
            yield Flake8Error.construct(
                func,
                610,
                f"function {func.name} allows for {num_positional} positional arguments,"
                f" a max of {max_positional} is permitted",
                cls,
            )

    @staticmethod
    def class_or_self(arg: Optional[ast.arg]) -> bool:
        if arg is None:
            return False
        return arg.arg in ("self", "cls")

    @staticmethod
    def first_arg(func: ast.FunctionDef | ast.AsyncFunctionDef) -> Optional[ast.arg]:
        if len(func.args.posonlyargs) > 0:
            return func.args.posonlyargs[0]
        elif len(func.args.args) > 0:
            return func.args.args[0]
        return None


class MaxPositionalArgsInInvocation:
    @classmethod
    def check(
        cls, invocation: ast.Call, max_positional: int
    ) -> Generator[Flake8Error, None, None]:
        if len(invocation.args) > max_positional:
            yield Flake8Error.construct(
                invocation,
                620,
                f"function called with {len(invocation.args)} positional arguments,"
                f" a max of {max_positional} is permitted",
                cls,
            )


class ConsecutiveSameTypedPositionalArgs:
    @classmethod
    def check(
        cls, func: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> Generator[Flake8Error, None, None]:
        # do not look at posonlyargs or kwonlyargs
        for arg_1, arg_2 in itertools.pairwise(func.args.args):
            annotation_1, annotation_2 = arg_1.annotation, arg_2.annotation
            if annotation_1 is not None and annotation_2 is not None:
                if ast.dump(annotation_1) == ast.dump(annotation_2):
                    yield Flake8Error.construct(
                        func,
                        630,
                        "function called with two consecutive positional arguments"
                        f" with identical typing: `{arg_1.arg}` and `{arg_2.arg}`",
                        cls,
                    )
