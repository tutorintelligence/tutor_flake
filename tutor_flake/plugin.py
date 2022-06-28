import ast
from argparse import Namespace
from dataclasses import dataclass
from typing import Any, Generator, List

from flake8.options.manager import OptionManager

from tutor_flake import __version__
from tutor_flake.common import Flake8Error
from tutor_flake.rules.asyncio import CreateTaskRequireName
from tutor_flake.rules.classvar import ClassvarOrderingAndInstanceOverlap
from tutor_flake.rules.dataclass import DataclassMissingAnnotations, DataclassRenamed
from tutor_flake.rules.no_sideeffects import NoSideeffects
from tutor_flake.rules.positional_args import MaxPostionalArgsInFunctionDef
from tutor_flake.rules.string import NoBracketInString


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
            default=3,
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
    name = "tutor_intelligence_custom_flake"
    version = __version__

    config: TutorFlakeConfig

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


class CustomVisitor(ast.NodeVisitor):
    def __init__(self, config: TutorFlakeConfig) -> None:
        self.errors: List[Flake8Error] = []
        self.config = config

    def visit_Module(self, node: ast.Module) -> Any:
        self.errors.extend(NoSideeffects.check(node))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.errors.extend(DataclassMissingAnnotations.check(node))
        self.errors.extend(ClassvarOrderingAndInstanceOverlap.check(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.errors.extend(DataclassRenamed.check(node))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.errors.extend(CreateTaskRequireName.check(node))
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        self.errors.extend(NoBracketInString.check(node))
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.errors.extend(
            MaxPostionalArgsInFunctionDef.check(
                node, self.config.max_definition_positional_args
            )
        )
        self.generic_visit(node)
