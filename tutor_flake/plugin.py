import ast
import itertools
from _ast import Expr, Name
from argparse import Namespace
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, ClassVar, Generator, Iterable, List, Optional, TypeVar

from flake8.options.manager import OptionManager
from typing_extensions import Self

from tutor_flake import __version__
from tutor_flake.common import Flake8Error
from tutor_flake.rules.asyncio import (
    AsyncFunctionsAreAsynchronous,
    CancelPassedMessage,
    CreateTaskIsAssigned,
    CreateTaskRequireName,
    HandlersAreSafeForCancelledErrors,
)
from tutor_flake.rules.classvar import ClassvarCheck
from tutor_flake.rules.compact_generic import CompactGeneric
from tutor_flake.rules.constructor import ConstructorIsWellTyped
from tutor_flake.rules.dataclass import DataclassRenamed
from tutor_flake.rules.no_sideeffects import NoSideeffects
from tutor_flake.rules.not_implemented import NotImplementedCheck
from tutor_flake.rules.os_path import (
    NoFromOSPathImports,
    NoOSPathAttrs,
    NoOSPathImports,
)
from tutor_flake.rules.positional_args import (
    ConsecutiveSameTypedPositionalArgs,
    MaxPositionalArgsInInvocation,
    MaxPostionalArgsInFunctionDef,
)
from tutor_flake.rules.string import NoBracketInString
from tutor_flake.rules.super import ChildClassCallsSuperMethods, NoTwoArgumentSuper
from tutor_flake.rules.time import NoFromTimeTimeImports, NoTimeDotTime


@dataclass
class TutorFlakeConfig:
    max_definition_positional_args: int
    max_invocation_positional_args: int
    non_init_classes: list[str]

    @staticmethod
    def add_options(option_manager: OptionManager) -> None:
        option_manager.add_option(
            short_option_name="-maxdefpos",
            long_option_name="--max_definition_positional_args",
            type=int,
            default=4,
            help="The max number of positional arguments a function can be defined with",
            required=False,
            parse_from_config=True,
        )
        option_manager.add_option(
            short_option_name="-maxinvocpos",
            long_option_name="--max_invocation_positional_args",
            type=int,
            default=4,
            help="The max number of positional arguments a function can be invoked with",
            required=False,
            parse_from_config=True,
        )
        option_manager.add_option(
            short_option_name="-ninitcls",
            long_option_name="--non_init_classes",
            default=[],
            comma_separated_list=True,
            parse_from_config=True,
            normalize_paths=True,
            help="Classes that are known to not have a meaningful `__init__`",
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> Self:
        return cls(
            options.max_definition_positional_args,
            options.max_invocation_positional_args,
            options.non_init_classes,
        )


class TutorIntelligenceFlakePlugin:
    name: ClassVar[str] = "tutor_intelligence_custom_flake"
    version: ClassVar[str] = __version__

    config: TutorFlakeConfig  # noqa: TUT503

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Flake8Error, None, None]:
        visitor = CustomVisitor(self.config)
        visitor.visit(self._tree)
        yield from visitor.errors

    @staticmethod
    def add_options(option_manager: OptionManager) -> None:
        TutorFlakeConfig.add_options(option_manager)

    @classmethod
    def parse_options(cls, options: Namespace) -> None:
        cls.config = TutorFlakeConfig.parse_options(options)


ASTLike = TypeVar("ASTLike", bound=ast.AST)


def visitor_decorator(
    func: Callable[["CustomVisitor", ASTLike], Iterable[Flake8Error]]
) -> Callable[["CustomVisitor", ASTLike], None]:
    @wraps(func)
    def wrapped_func(visitor: "CustomVisitor", node: ASTLike) -> None:
        visitor.errors.extend(func(visitor, node))
        with visitor.add_parent(node):
            visitor.generic_visit(node)

    return wrapped_func


class CustomVisitor(ast.NodeVisitor):
    def __init__(self, config: TutorFlakeConfig) -> None:
        self.errors: List[Flake8Error] = []
        self.config = config
        # list of parent nodes of the currently visited node
        # with the most immediate parent last
        self.parents: List[ast.AST] = []

        super().__init__()

    @property
    def parent(self) -> Optional[ast.AST]:
        return None if len(self.parents) == 0 else self.parents[-1]

    @contextmanager
    def add_parent(self, node: ast.AST) -> Generator[None, Any, Any]:
        """Adds node to the list of parents"""
        self.parents.append(node)
        yield
        self.parents.pop()

    @visitor_decorator
    def visit_Module(self, node: ast.Module) -> Iterable[Flake8Error]:
        return NoSideeffects.check(node)

    @visitor_decorator
    def visit_ClassDef(self, node: ast.ClassDef) -> Iterable[Flake8Error]:
        return ClassvarCheck.check(node)

    @visitor_decorator
    def visit_Import(self, node: ast.Import) -> Iterable[Flake8Error]:
        return NoOSPathImports.check(node)

    @visitor_decorator
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Iterable[Flake8Error]:
        return itertools.chain(
            DataclassRenamed.check(node),
            NoFromOSPathImports.check(node),
            NoFromTimeTimeImports.check(node),
        )

    @visitor_decorator
    def visit_Call(self, node: ast.Call) -> Iterable[Flake8Error]:
        return itertools.chain(
            CreateTaskRequireName.check(node),
            MaxPositionalArgsInInvocation.check(
                node, self.config.max_invocation_positional_args
            ),
            NoTwoArgumentSuper.check(node, self.parents),
            CancelPassedMessage.check(node),
        )

    @visitor_decorator
    def visit_Constant(self, node: ast.Constant) -> Iterable[Flake8Error]:
        return NoBracketInString.check(node)

    @visitor_decorator
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[Flake8Error]:
        return itertools.chain(
            MaxPostionalArgsInFunctionDef.check(
                node, self.config.max_definition_positional_args
            ),
            ConsecutiveSameTypedPositionalArgs.check(node),
            ChildClassCallsSuperMethods.check(
                node, self.parents, self.config.non_init_classes
            ),
            ConstructorIsWellTyped.check(node, self.parents),
        )

    @visitor_decorator
    def visit_Attribute(self, node: ast.Attribute) -> Iterable[Flake8Error]:
        return itertools.chain(
            NoOSPathAttrs.check(node),
            NoTimeDotTime.check(node),
        )

    @visitor_decorator
    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[Flake8Error]:
        return CompactGeneric.check(node, self.parent)

    @visitor_decorator
    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> Iterable[Flake8Error]:
        return itertools.chain(
            MaxPostionalArgsInFunctionDef.check(
                node, self.config.max_definition_positional_args
            ),
            ConsecutiveSameTypedPositionalArgs.check(node),
            AsyncFunctionsAreAsynchronous.check(node),
            ConstructorIsWellTyped.check(node, self.parents),
        )

    @visitor_decorator
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> Iterable[Flake8Error]:
        return HandlersAreSafeForCancelledErrors.check_except_handler(node)

    @visitor_decorator
    def visit_Try(self, node: ast.Try) -> Iterable[Flake8Error]:
        return HandlersAreSafeForCancelledErrors.check_finally_body(node)

    @visitor_decorator
    def visit_Expr(self, node: Expr) -> Iterable[Flake8Error]:
        return CreateTaskIsAssigned.check(node)

    @visitor_decorator
    def visit_Name(self, node: Name) -> Iterable[Flake8Error]:
        return NotImplementedCheck.check(node, self.parents)
