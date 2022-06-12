import argparse
import ast
import subprocess

import astpretty


def isort() -> None:
    subprocess.run(["isort", "."], check=True)


def black() -> None:
    subprocess.run(["black", "."], check=True)


def flake8() -> None:
    subprocess.run(["flake8"], check=True)


def mypy() -> None:
    subprocess.run(["mypy", "."], check=True)


def _get_code_file(description: str) -> ast.Module:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("file", type=str)
    with open(parser.parse_args().file) as f:
        return ast.parse(f.read())


def print_ast() -> None:
    astpretty.pprint(_get_code_file("Pretty print AST of file"))


def style() -> None:
    isort()
    black()
    flake8()
    mypy()
