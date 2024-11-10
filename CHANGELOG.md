# Changelog

<!--next-version-placeholder-->

## v0.26.2 (2024-11-10)
### Fix
* Handle attribute error in more cases ([`469852a`](https://github.com/tutorintelligence/tutor_flake/commit/469852a1e79b6954c99b1e84d907f990ba187bcf))

## v0.26.1 (2024-11-10)
### Fix
* Handle attribute error ([`b6b0632`](https://github.com/tutorintelligence/tutor_flake/commit/b6b063218ef495549686bd23846fe996609847cb))

## v0.26.0 (2024-08-24)
### Feature
* Add rule enforces Self types on constructors ([#20](https://github.com/tutorintelligence/tutor_flake/issues/20)) ([`9f7d044`](https://github.com/tutorintelligence/tutor_flake/commit/9f7d044f8dd3c752f8d430e2e93a6ecfef3f85be))

## v0.25.1 (2024-08-13)
### Fix
* Allow for function which have docstrings, but are also basic. ([#19](https://github.com/tutorintelligence/tutor_flake/issues/19)) ([`bab85cc`](https://github.com/tutorintelligence/tutor_flake/commit/bab85cce37c4257db3090bfe1410a7433d6ed0f8))

## v0.25.0 (2024-06-13)
### Feature
* Skip more collections ([#18](https://github.com/tutorintelligence/tutor_flake/issues/18)) ([`0d1abb0`](https://github.com/tutorintelligence/tutor_flake/commit/0d1abb0bb3da75d04df32099c6b9f86af3c94dde))

## v0.24.0 (2024-06-07)
### Feature
* Prevent consecutive same typed positional arguments ([#17](https://github.com/tutorintelligence/tutor_flake/issues/17)) ([`53d152e`](https://github.com/tutorintelligence/tutor_flake/commit/53d152e29865a265cb8dc62938283d4ea3a1a861))

## v0.23.1 (2024-06-07)
### Fix
* Max positional args in async function def ([#16](https://github.com/tutorintelligence/tutor_flake/issues/16)) ([`21c83d8`](https://github.com/tutorintelligence/tutor_flake/commit/21c83d8cbbac8411eb9a66f35548f86321c0d1eb))

## v0.23.0 (2024-06-07)
### Feature
* Separate error for missing super calls and better configurability ([#15](https://github.com/tutorintelligence/tutor_flake/issues/15)) ([`f8674b7`](https://github.com/tutorintelligence/tutor_flake/commit/f8674b7413b4941b5850b0b2d454e71bf2d4e005))

## v0.22.0 (2023-12-19)
### Feature
* Added carveout from classvar rule for pydantic BaseModel ([#14](https://github.com/tutorintelligence/tutor_flake/issues/14)) ([`5f74626`](https://github.com/tutorintelligence/tutor_flake/commit/5f7462673f928cd96533a40067dcfae64df76272))

## v0.21.0 (2023-09-28)
### Feature
* Enforce reasonable use of NotImplemented ([#13](https://github.com/tutorintelligence/tutor_flake/issues/13)) ([`c6eff7b`](https://github.com/tutorintelligence/tutor_flake/commit/c6eff7bcef423f14a0abe9ca6268faca4efc459f))

## v0.20.3 (2023-08-28)
### Fix
* Actually broaden excluded classes from super init enforcement ([`533df68`](https://github.com/tutorintelligence/tutor_flake/commit/533df68c6b9284fa0e5433f6033eec93123cdbe8))

## v0.20.2 (2023-08-28)
### Fix
* Broaden excluded classes from super init enforcement ([`e21baef`](https://github.com/tutorintelligence/tutor_flake/commit/e21baef7317698b073917dc7d863b84bca819923))

## v0.20.1 (2023-08-28)
### Fix
* Allow no super inits in generics ([`e352982`](https://github.com/tutorintelligence/tutor_flake/commit/e352982ad928d33001bb935d82b2b4f5e1e8099a))

## v0.20.0 (2023-08-28)
### Feature
* Enforce init and post_init are called in subclasses ([#12](https://github.com/tutorintelligence/tutor_flake/issues/12)) ([`f35e5ba`](https://github.com/tutorintelligence/tutor_flake/commit/f35e5bad60ac48fb6022a5b55ba7652a9c3da98c))

## v0.19.0 (2023-08-03)
### Feature
* Require passing msgs to cancel calls ([#11](https://github.com/tutorintelligence/tutor_flake/issues/11)) ([`c32e550`](https://github.com/tutorintelligence/tutor_flake/commit/c32e5504803e49f004624dd020f914ac1a722a87))

## v0.18.1 (2023-08-01)
### Fix
* Allowing typing class variables as Final ([#10](https://github.com/tutorintelligence/tutor_flake/issues/10)) ([`58dc1f2`](https://github.com/tutorintelligence/tutor_flake/commit/58dc1f29a7fe0280c3f14e5542e4c9190c44f03e))

## v0.18.0 (2023-08-01)
### Feature
* Prevent time.time and suggest alternatives ([#9](https://github.com/tutorintelligence/tutor_flake/issues/9)) ([`45bb875`](https://github.com/tutorintelligence/tutor_flake/commit/45bb875c669735d4b2a2dc9b4f604886b813a86b))

### Documentation
* Add motiviation for rule 201 ([`b23d25e`](https://github.com/tutorintelligence/tutor_flake/commit/b23d25e4ee9dc444d7d402b3ab3e256779d91b93))

## v0.17.0 (2023-05-12)
### Feature
* Enforce that async tasks are not dropped ([`7d83116`](https://github.com/tutorintelligence/tutor_flake/commit/7d83116e3ec8483e1db86ff33ab302b5519b6bf0))

## v0.16.0 (2023-05-12)
### Feature
* Change code from TUTOR to TUT ([`b0653f9`](https://github.com/tutorintelligence/tutor_flake/commit/b0653f9a37c40e5522d1ed305aceca6dcb727648))

## v0.15.1 (2023-03-23)
### Fix
* Classvar and type annotation rules apply correctly ([#7](https://github.com/tutorintelligence/tutor_flake/issues/7)) ([`f23b344`](https://github.com/tutorintelligence/tutor_flake/commit/f23b344a18905dc65cade6cc449a9a836e9eb88b))

## v0.15.0 (2023-03-23)
### Feature
* Update python version and flake version ([#6](https://github.com/tutorintelligence/tutor_flake/issues/6)) ([`6d9c9f2`](https://github.com/tutorintelligence/tutor_flake/commit/6d9c9f235fb5a954f3c2c2116490d643ba63e6ce))

## v0.14.2 (2022-11-11)
### Fix
* Only trigger error in correct catch blocks ([`a49de82`](https://github.com/tutorintelligence/tutor_flake/commit/a49de82ebc3da64f5e33729d8465d412e8c053fb))
* Only trigger error in correct catch blocks ([`16ecb90`](https://github.com/tutorintelligence/tutor_flake/commit/16ecb9001cbfa23acb57c9715706901a06908cc2))

## v0.14.1 (2022-11-11)
### Fix
* Allow asyncio sleep in exception handling ([`f3daf2e`](https://github.com/tutorintelligence/tutor_flake/commit/f3daf2e411af012ffbeaab8f43e584944d0d89a2))

## v0.14.0 (2022-11-11)
### Feature
* Prevent hanging async processes post cancellation ([`77b433c`](https://github.com/tutorintelligence/tutor_flake/commit/77b433ca041baad47b8542213c957acbb57b7b98))

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
