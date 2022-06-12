import ast
from enum import Enum
from typing import Generator, List, NamedTuple

from tutor_flake import __version__


class Flake8Error(NamedTuple):
    line_number: int
    offset: int
    msg: str
    cls: type  # currently unused but required


ErrorDescriptions = ["100 Dataclass missing annotation for a class variable"]


class CustomError(Enum):
    DATACLASS_MISSING_ANNOTATIONS = 0

    def __str__(self) -> str:
        return f"TUTOR{ErrorDescriptions[self.value]}"


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

    @classmethod
    def get_error(
        cls, line_number: int, offset: int, error: CustomError
    ) -> Flake8Error:
        return Flake8Error(line_number, offset, str(error), cls)

    def add_error(self, node: ast.AST, error: CustomError) -> None:
        self.errors.append(self.get_error(node.lineno, node.col_offset, error))

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        if is_dataclass(node):
            for child in node.body:
                if isinstance(child, ast.Assign) and child.type_comment is None:
                    self.add_error(child, CustomError.DATACLASS_MISSING_ANNOTATIONS)
        self.generic_visit(node)


def is_dataclass(node: ast.ClassDef) -> bool:
    for decorator in node.decorator_list:
        if (
            isinstance(decorator, ast.Name)
            and decorator.id == "dataclass"
            and isinstance(decorator.ctx, ast.Load)
        ):
            return True
    return False
