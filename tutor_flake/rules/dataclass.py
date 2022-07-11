import ast
from typing import Generator

from tutor_flake.common import Flake8Error


class DataclassRenamed:
    @classmethod
    def check(cls, node: ast.ImportFrom) -> Generator[Flake8Error, None, None]:
        if node.module == "dataclasses":
            for name in node.names:
                if name.name == "dataclass" and name.asname is not None:
                    yield Flake8Error.construct(
                        node, "101", "Dataclass renamed on import", cls
                    )
