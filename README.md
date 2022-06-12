# tutor_flake

Custom flake8 rules

## Rules

* TUTOR100 - dataclass class variables require annotations
    * Notes: you can trick this rule by renaming dataclass - and there is the potential for some false positives
* TUTOR101 - dataclasses.dataclass cannot be renamed in import
    * Notes: this is meant to act against the major case of false negatives for TUTOR100
* TUTOR200 - asyncio.create_task requires the name parameter

## Future Ideas

* Max number of positional arguments to function
    * In definition or invocation
* Enforce calling await on async methods
    * I would like to do this - but I don't know how to identify if a method is async