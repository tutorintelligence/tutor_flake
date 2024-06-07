import ast

from tutor_flake.common import Flake8Error, check_any_parent

STANDARD_MSG = "This very likely is not what you want."


class NotImplementedCheck:
    @classmethod
    def check(cls, node: ast.Name, parents: list[ast.AST]) -> list[Flake8Error]:
        error = cls.check_node(node, parents)
        return [] if error is None else [error]

    @classmethod
    def check_node(cls, node: ast.Name, parents: list[ast.AST]) -> Flake8Error | None:
        if node.id != "NotImplemented" or not isinstance(node.ctx, ast.Load):
            return None
        reversed_parents = reversed(parents)
        for parent_i, parent in enumerate(reversed_parents):
            if isinstance(parent, ast.FunctionDef):
                if not parent.name.startswith("__") or not parent.name.endswith("__"):
                    return Flake8Error.construct(
                        node,
                        520,
                        "You are using NotImplemented in a non-dunder"
                        f" function call: `{parent.name}`. {STANDARD_MSG}",
                        cls,
                    )
                elif not check_any_parent(parents[parent_i + 1 :], ast.ClassDef):
                    return Flake8Error.construct(
                        node,
                        520,
                        "You are using NotImplemented in a dunder function"
                        f" call outside of a class. {STANDARD_MSG}",
                        cls,
                    )
                return None
        else:
            return Flake8Error.construct(
                node,
                520,
                f"You are using NotImplemented outside of a function call. {STANDARD_MSG}",
                cls,
            )
