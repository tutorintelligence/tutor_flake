# tutor_flake

Custom flake8 rules

## Rules

* TUT100 (DEPRECATED, covered by 502) - dataclass class variables require annotations
    * Notes: you can trick this rule by renaming dataclass - and there is the potential for some false positives
* TUT101 - dataclasses.dataclass cannot be renamed in import
    * Notes: this is meant to act against the major case of false negatives for TUT100
* TUT2:
    * TUT200 - asyncio.create_task requires the name parameter
    * TUT201 - asyncio.create_task is either `await`ed or assigned to a variable
        * See `Important` [here](https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task) on garbage collection for motivation
    * TUT210 - async function call either `await` or `async for` or `async with`
        * If the body of the function is either `pass` or immediately errors or immediately returns, the function is excused
        * It is expected that some class functions will fail this rule, but it still has utility
    * TUT220 - no async function in a `catch` block that will catch a cancelled error or `finally` that is not one of `asyncio.wait_for`, `asyncio.wait` or `asyncio.sleep`, prevents running forever when task is cancelled
    * TUT230 - any call to `cancel` is passed a message (that is not a `None` literal)
        * This is a highly opinionated as it assumes that any `cancel` call that matches the spec of `asyncio.Task.cancel` is on a task.  To enforce this properly you would use typing, but that is a more aggressive step to take
* TUT300 - no expressions in the main body, unless under __name__ == "__main__", prevents global side effects
* TUT4:
    * TUT400 - detect strings that were likely meant to be f-strings
    * TUT410 - detect redundant type annotations
    * TUT411 - detect redundant type annotations for generic assignment
        * Don't do `x: Foo[bar] = Foo()` ; do `x = Foo[bar]()`
* TUT5
    * TUT500 (DEPRECATED: covered by 502/503 + mypy) - instance variables set in `__init__` cannot overlap with class variables
    * TUT501 - class variables must be defined before all functions
    * TUT502 - class variables must be type annotated
        * with exceptions for Enum and IntEnum
        * It is safe to ignore this rule in the case where the variable is inherited - this is hard to detect in flake though
    * TUT503 - class variables must be annotated as ClassVar or Final, with exceptions for:
        * dataclasses
        * NamedTuple
        * Protocol
        * Enum and IntEnum
        * TypedDict
        * pydantic BaseModel
    * TUT510 - No two argument `super` within a class
    * TUT511 - A child class must call a parent classes method for `__init__` and `__post_init__`
    * TUT520 - `NotImplemented` is only allowed within a dunder method on a class
        * Any other usage is very likely incorrect
* TUT6
    * TUT610 - a function definition allows too many positional arguments (configurable with `max-definition-positional-args`)
    * TUT620 - a function invocation uses too many positional arguments (configurable with `max-invocation-positional-args`)
* TUT7
    * TUT700 - Prevent `os.path.<func>()` function calls
    * TUT710 - Prevent `from os import path`
    * TUT720 - Prevent `import os.path`
* TUT8
    * TUT800 - Prevent `time.time`
        * Note: programmers often use `time.time` to extract time deltas in seconds, rather than actually fetching the numbers of seconds since the epoch.  This has tricky pitfalls, such as clock sync jumps and lack of monotonicity guarantees.
    * TUT810 - Prevent `from time import time` (see TUT800)

## Future Ideas

* Enforce calling await on async methods
    * I would like to do this - but I don't know how to identify if a method is async
* No adjacent positional arguments with same typing - unless positional only
* No addition of string literals (or f-strings)
* Should we also forbid `os.walk`
* Fixtures must end in `_fixt`
* Constants must be uppercase

## Installation and Configuration

In a pyproject.toml, can install like this:
```
tutor-flake = {git = "ssh://git@github.com/tutorintelligence/tutor_flake.git", rev = "v0.2.0"}
```

To configure, in `setup.cfg`
```
[flake8:local-plugins]
extension = 
    TUT = tutor_flake.plugin:TutorIntelligenceFlakePlugin
```