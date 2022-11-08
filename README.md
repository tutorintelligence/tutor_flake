# tutor_flake

Custom flake8 rules

## Rules

* TUTOR100 (DEPRECATED, covered by 502) - dataclass class variables require annotations
    * Notes: you can trick this rule by renaming dataclass - and there is the potential for some false positives
* TUTOR101 - dataclasses.dataclass cannot be renamed in import
    * Notes: this is meant to act against the major case of false negatives for TUTOR100
* TUTOR2:
    * TUTOR200 - asyncio.create_task requires the name parameter
    * TUTOR210 - async function call either `await` or `async for` or `async with`
        * If the body of the function is either `pass` or immediately errors, the function is excused
        * It is expected that some class functions will fail this rule, but it still has utility
* TUTOR300 - no expressions in the main body, unless under __name__ == "__main__", prevents global side effects
* TUTOR4:
    * TUTOR400 - detect strings that were likely meant to be f-strings
    * TUTOR410 - detect redundant type annotations
    * TUTOR411 - detect redundant type annotations for generic assignment
        * Don't do `x: Foo[bar] = Foo()` ; do `x = Foo[bar]()`
* TUTOR5
    * TUTOR500 (DEPRECATED: covered by 502/503 + mypy) - instance variables set in `__init__` cannot overlap with class variables
    * TUTOR501 - class variables must be defined before all functions
    * TUTOR502 - class variables must be type annotated
        * with exceptions for Enum and IntEnum
        * It is safe to ignore this rule in the case where the variable is inherited - this is hard to detect in flake though
    * TUTOR503 - class variables must be annotated as class variables, with exceptions for:
        * dataclasses
        * NamedTuple
        * Protocol
        * Enum and IntEnum
        * TypedDict
    * TUTOR510 - No two argument `super` within a class
* TUTOR6
    * TUTOR610 - a function definition allows too many positional arguments (configurable with `max-definition-positional-args`)
    * TUTOR620 - a function invocation uses too many positional arguments (configurable with `max-invocation-positional-args`)
* TUTOR7
    * TUTOR700 - Prevent `os.path.<func>()` function calls
    * TUTOR710 - Prevent `from os import path`
    * TUTOR720 - Prevent `import os.path`

## Future Ideas

* Enforce calling await on async methods
    * I would like to do this - but I don't know how to identify if a method is async
* No adjacent positional arguments with same typing - unless positional only
* No addition of string literals (or f-strings)
* Should we also forbid `os.walk`

## Installation and Configuration

In a pyproject.toml, can install like this:
```
tutor-flake = {git = "ssh://git@github.com/tutorintelligence/tutor_flake.git", rev = "v0.2.0"}
```

To configure, in `setup.cfg`
```
[flake8:local-plugins]
extension = 
    TUTOR = tutor_flake.plugin:TutorIntelligenceFlakePlugin
```