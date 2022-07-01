import ast
from typing import Generator

from tutor_flake.common import Flake8Error


class NoOSPathAttrs:
    @classmethod
    def check(cls, attr: ast.Attribute) -> Generator[Flake8Error, None, None]:
        if (
            attr.attr == "path"
            and isinstance(attr.value, ast.Name)
            and attr.value.id == "os"
        ):
            yield Flake8Error.construct(
                attr,
                "700",
                "OS Path must be replaced with pathlib. Remove all instances of os.path.<func>()",
                cls,
            )


class NoFromOSPathImports:
    @classmethod
    def check(cls, node: ast.ImportFrom) -> Generator[Flake8Error, None, None]:
        import_path_from_os_cond = node.module == "os" and any(
            [name.name == "path" for name in node.names]
        )
        import_func_from_os_path_cond = "os.path" in node.module
        if import_func_from_os_path_cond or import_path_from_os_cond:
            yield Flake8Error.construct(
                node,
                "710",
                "OS Path must be replaced with pathlib. Do not import os.path!",
                cls,
            )


class NoOSPathImports:
    @classmethod
    def check(cls, node: ast.Import) -> Generator[Flake8Error, None, None]:
        if any(["os.path" in name.name for name in node.names]):
            yield Flake8Error.construct(
                node,
                "720",
                "OS Path must be replaced with pathlib. Do not import os.path!",
                cls,
            )
