import ast
from typing import Generator, List

from tutor_flake import __version__
from tutor_flake.common import Flake8Error
from tutor_flake.rules.asyncio import CreateTaskRequireName
from tutor_flake.rules.dataclass import DataclassMissingAnnotations, DataclassRenamed


class TutorIntelligenceFlakePlugin:
    name = "tutor_intelligence_custom_flake"
    version = __version__

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Flake8Error, None, None]:
        visitor = CustomVisitor()
        visitor.visit(self._tree)
        yield from visitor.errors


class CustomVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Flake8Error] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.errors.extend(DataclassMissingAnnotations.check(node))
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.errors.extend(DataclassRenamed.check(node))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.errors.extend(CreateTaskRequireName.check(node))
        self.generic_visit(node)
