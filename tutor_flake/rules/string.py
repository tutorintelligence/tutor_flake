import ast
from typing import Generator

from tutor_flake.common import Flake8Error


class NoBracketInString:
    """Errors on strings that were likely meant to be f-strings"""

    @classmethod
    def check(cls, node: ast.Constant) -> Generator[Flake8Error, None, None]:
        if isinstance(msg := node.value, str) and cls.has_bounding_brackets(msg):
            yield Flake8Error.construct(
                node,
                "400",
                f"String `{msg}` contains brackets, likely meant to be an f-string",
                cls,
            )

    @classmethod
    def has_bounding_brackets(cls, msg: str) -> bool:
        if "{" in msg and "}" in msg:
            left_bracket_i = msg.find("{")
            right_bracket_i = len(msg) - 1 - msg[::-1].find("}")
            return left_bracket_i < right_bracket_i
        return False
