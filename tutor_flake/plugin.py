import ast
import itertools
from argparse import Namespace
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, ClassVar, Generator, Iterable, List, Optional, TypeVar

from flake8.options.manager import OptionManager

from tutor_flake import __version__
from tutor_flake.common import Flake8Error
from tutor_flake.rules.asyncio import (
    AsyncFunctionsAreAsynchronous,
    CreateTaskRequireName,
    HandlersAreSafeForCancelledErrors,
)
from tutor_flake.rules.classvar import ClassvarCheck
from tutor_flake.rules.compact_generic import CompactGeneric
from tutor_flake.rules.dataclass import DataclassRenamed
from tutor_flake.rules.no_sideeffects import NoSideeffects
from tutor_flake.rules.os_path import (
    NoFromOSPathImports,
    NoOSPathAttrs,
    NoOSPathImports,
)
from tutor_flake.rules.positional_args import (
    MaxPositionalArgsInInvocation,
    MaxPostionalArgsInFunctionDef,
)
from tutor_flake.rules.string import NoBracketInString
from tutor_flake.rules.super import NoTwoArgumentSuper


@dataclass
class TutorFlakeConfig:
    max_definition_positional_args: int
    max_invocation_positional_args: int

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

    @classmethod
    def parse_options(cls, options: Namespace) -> "TutorFlakeConfig":
        return TutorFlakeConfig(
            options.max_definition_positional_args,
            options.max_invocation_positional_args,
        )


class TutorIntelligenceFlakePlugin:
    name: ClassVar[str] = "tutor_intelligence_custom_flake"
    version: ClassVar[str] = __version__

    config: TutorFlakeConfig  # noqa: TUTOR503

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

        self.parents: List[ast.AST] = []

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
        )

    @visitor_decorator
    def visit_Call(self, node: ast.Call) -> Iterable[Flake8Error]:
        return itertools.chain(
            CreateTaskRequireName.check(node),
            MaxPositionalArgsInInvocation.check(
                node, self.config.max_invocation_positional_args
            ),
            NoTwoArgumentSuper.check(node, self.parents),
        )

    @visitor_decorator
    def visit_Constant(self, node: ast.Constant) -> Iterable[Flake8Error]:
        return NoBracketInString.check(node)

    @visitor_decorator
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Iterable[Flake8Error]:
        return MaxPostionalArgsInFunctionDef.check(
            node, self.config.max_definition_positional_args
        )

    @visitor_decorator
    def visit_Attribute(self, node: ast.Attribute) -> Iterable[Flake8Error]:
        return NoOSPathAttrs.check(node)

    @visitor_decorator
    def visit_AnnAssign(self, node: ast.AnnAssign) -> Iterable[Flake8Error]:
        return CompactGeneric.check(node, self.parent)

    @visitor_decorator
    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> Iterable[Flake8Error]:
        return AsyncFunctionsAreAsynchronous.check(node)

    @visitor_decorator
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> Iterable[Flake8Error]:
        return HandlersAreSafeForCancelledErrors.check_except_handler(node)

    @visitor_decorator
    def visit_Try(self, node: ast.Try) -> Iterable[Flake8Error]:
        return HandlersAreSafeForCancelledErrors.check_finally_body(node)
