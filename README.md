# tutor_flake

Custom flake8 rules

## Rules

* TUTOR100 - dataclass class variables require annotations
    * Notes: you can trick this rule by renaming dataclass - and there is the potential for some false positives
* TUTOR101 - dataclasses.dataclass cannot be renamed in import
    * Notes: this is meant to act against the major case of false negatives for TUTOR100
* TUTOR200 - asyncio.create_task requires the name parameter
* TUTOR300 - no expressions in the main body, unless under __name__ == "__main__", prevents global side effects
* TUTOR400 - detect strings that were likely meant to be f-strings
* TUTOR500 - instance variables set in `__init__` cannot overlap with class variables
    * TUTOR501 - class variables must be defined before all functions
* TUTOR6
    * TUTOR610 - a function definition allows too many positional arguments (configurable with `max-definition-positional-args`)
    * TUTOR620 - a function invocation uses too many positional arguments (configurable with `max-invocation-positional-args`)
    * TUTOR700 - Prevent `os.path.<func>()` function calls
    * TUTOR710 - Prevent `from os import path`
    * TUTOR720 - Prevent `import os.path`

## Future Ideas

* Enforce calling await on async methods
    * I would like to do this - but I don't know how to identify if a method is async
* No adjacent positional arguments with same typing - unless positional only

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