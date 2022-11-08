# Changelog

<!--next-version-placeholder-->

## v0.13.0 (2022-11-08)
### Feature
* Async allow immediate return ([`44d030c`](https://github.com/tutorintelligence/tutor_flake/commit/44d030c371a4bcef8af6cc791fa0a77b52ba148d))

## v0.12.0 (2022-11-08)
### Feature
* Check all async functions are meaningful asynchronous ([#5](https://github.com/tutorintelligence/tutor_flake/issues/5)) ([`0cfec44`](https://github.com/tutorintelligence/tutor_flake/commit/0cfec44319165e01a24d207fccf9ba4069614adf))

## v0.11.1 (2022-07-30)
### Fix
* Expections to compact generic rule ([`f51a678`](https://github.com/tutorintelligence/tutor_flake/commit/f51a678c4ad0ff53339fa8f1c8f9f6b59af88193))

## v0.11.0 (2022-07-29)
### Feature
* Forbid redundant type annotations ([`a797e94`](https://github.com/tutorintelligence/tutor_flake/commit/a797e94f9a6d51ca24775e59f6d3675c5b0bb2d8))

## v0.10.4 (2022-07-12)
### Fix
* Except Enum from 502 as well ([`0a725fb`](https://github.com/tutorintelligence/tutor_flake/commit/0a725fbb165e92bc6fcaaa8a315974b327830492))

## v0.10.3 (2022-07-12)
### Fix
* Ignore classvar on TypedDict ([`9c510ab`](https://github.com/tutorintelligence/tutor_flake/commit/9c510ab58846d65b59bed41fe66c9c05810a7531))

## v0.10.2 (2022-07-11)
### Fix
* Allow Enum to not be ClassVar annotatted ([`c3f7bd0`](https://github.com/tutorintelligence/tutor_flake/commit/c3f7bd0cfd50a5a84b827393ec4a3dffa9915406))

## v0.10.1 (2022-07-11)
### Fix
* Exception for Protocol ([`83ecb47`](https://github.com/tutorintelligence/tutor_flake/commit/83ecb47f688396c205e73efd620dbe939ca714ad))

## v0.10.0 (2022-07-11)
### Feature
* Require class var annotations for class variables ([`240930f`](https://github.com/tutorintelligence/tutor_flake/commit/240930f971d6657e94071b66569718aede315f27))

## v0.9.1 (2022-07-07)
### Fix
* Dont check multiline string - often no way to noqa ([`213a852`](https://github.com/tutorintelligence/tutor_flake/commit/213a852ef3dce4241fa5c29735b837353410256d))

## v0.9.0 (2022-07-07)
### Feature
* Rule against two argument super usage ([`b51e323`](https://github.com/tutorintelligence/tutor_flake/commit/b51e323a25892fc814eabc86ef41d242b0f41356))

## v0.8.1 (2022-07-05)
### Fix
* Allow untyped variables in dataclass if they are typevars ([`6c78a8b`](https://github.com/tutorintelligence/tutor_flake/commit/6c78a8bca74ef8ceaff95f74952c012f9781fa83))

## v0.8.0 (2022-07-01)
### Feature
* Remove OS.path from all repos ([`402c677`](https://github.com/tutorintelligence/tutor_flake/commit/402c6771998e673263432db01b2f0335f5d5c1f8))
* Remove OS.path from all repos ([`1beb1f4`](https://github.com/tutorintelligence/tutor_flake/commit/1beb1f452ede6ba3c66ffd5b701167ac97bf52fa))
* Remove OS.path from all repos ([`4bece8c`](https://github.com/tutorintelligence/tutor_flake/commit/4bece8ca50cd72b9a9870c683cca76b2daec82bd))
* Remove OS.path from all repos ([`1ffa814`](https://github.com/tutorintelligence/tutor_flake/commit/1ffa8146daf6fe35277159df8d637dbd5302b40e))

## v0.7.0 (2022-06-28)
### Feature
* Configure max number of possitional arguments ([`281129d`](https://github.com/tutorintelligence/tutor_flake/commit/281129da5db6a2d66975e95d5681c7041ecdf165))

## v0.6.0 (2022-06-28)
### Feature
* Max number of positional arguments in function definition ([`ff68636`](https://github.com/tutorintelligence/tutor_flake/commit/ff686367c57d661f31d8aeb6b7909385075cd2e1))

## v0.5.0 (2022-06-28)
### Feature
* Instance variables and class variables should not overlap ([`1055bde`](https://github.com/tutorintelligence/tutor_flake/commit/1055bde4f8c96bcb47ef55bfe7ea4d2e06a90e32))

## v0.4.0 (2022-06-28)
### Feature
* False f-string detector rule ([`7ebe3eb`](https://github.com/tutorintelligence/tutor_flake/commit/7ebe3eb0a5d4abc581968eca3c41c48af109345a))

## v0.3.1 (2022-06-28)
### Fix
* Frozen dataclasses also require classvar ([`04897eb`](https://github.com/tutorintelligence/tutor_flake/commit/04897ebcae67bb57339a6da42c66b0a2b297c056))

## v0.3.0 (2022-06-27)
### Feature
* Prevent expressions in main body ([`7d6ea8d`](https://github.com/tutorintelligence/tutor_flake/commit/7d6ea8d7bb6e6b89f9fcca7862c82dfd4085f2e9))

## v0.2.0 (2022-06-13)
### Feature
* Setup github and workflow ([`7626479`](https://github.com/tutorintelligence/tutor_flake/commit/762647920cd3ebcff6394950fdab30598b1924a4))

### Fix
* Semantic release has correct path ([`36518b4`](https://github.com/tutorintelligence/tutor_flake/commit/36518b4081619116ae181725a7571e53ab2a994c))
* Add semantic release section ([`99dd840`](https://github.com/tutorintelligence/tutor_flake/commit/99dd840f960a5a63895a118f7a19d5fee242aee4))
