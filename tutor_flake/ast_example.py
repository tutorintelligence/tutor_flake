import ast


def main() -> None:
    with open("tutor_flake/example_code/dummy_code.py") as f:
        code = f.read()

    node = ast.parse(code)
    print(node)
    print(node._fields)
    print(node.body)


if __name__ == "__main__":
    main()
