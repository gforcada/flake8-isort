# Changelog

## 7.1.1 (unreleased)


- Nothing changed yet.


## 7.1.0 (2026-11-02)

- update supported python versions (3.11 to 3.15) @gforcada

- improve CI speed by using `uvx` and `prek` @gforcada

- tighten GHA with `zizmor` @gforcada

## 7.0.0 (2025-10-25)

- add support for isort 7.0.0 @gforcada

- drop python 3.9 support and add Python 3.14 support @gforcada

- bump pypy minimum version to 3.10

## 6.1.2 (2025-01-29)

- Add support for isort 6.0.0 @SukiCZ

- Drop python 3.8, and add python 3.13 @SukiCZ

## 6.1.1 (2023-11-03)

- switch from `setup.cfg` to `setup.py` @deronnax

- switch from `setuptools` to `hatchling` @gforcada

- switch to `main` branch @gforcada

- use `tox` and `pre-commit` to ease project maintenance @gforcada

## 6.1.0 (2023-09-15)

- drop python 3.7 support @gforcada

- add preliminary support to Python 3.12 @gforcada

## 6.0.0 (2022-12-22)

- drop isort 4.x support @gforcada

- add support for flake8 6.0.0 @gforcada

- add `--isort-no-skip-gitignore` option to allow temporarily overriding the set
  value of isort's `skip_gitignore` option with `False`. This can cause
  flake8-isort to run significantly faster at the cost of making flake8-isort's
  behavior differ slightly from the behavior of `isort --check` @gschaffner

## 5.0.3 (2022-11-20)

- fix broken `add_options` method, again. @casperdcl

## 5.0.2 (2022-11-19)

- fix broken `add_options` method @casperdcl

## 5.0.1 (2022-11-18)

- improve the config option is added and read back @gforcada

- bump plugin version @gforcada

## 5.0.0 (2022-10-08)

- update dependencies @gforcada

- revamp GitHub actions @gforcada

- drop python 3.6, and add python 3.10 @gforcada

- use linters and formatters to keep code sane and beautiful @gforcada

## 4.2.0 (2022-08-04)

- fix compatibility with flake8 version 5. @nhymxu

## 4.1.2.post0 (2022-07-25)

- release it as a wheel as well @gforcada

## 4.1.2 (2022-07-25)

- the package no longer depends on `testfixtures`

## 4.1.1 (2021-10-14)

- Release py3 only wheels..

## 4.1.0 (2021-10-14)

- support flake8 4.x @g-as

- switch from travis-ci to github actions. @g-as

- drop python 2.7 support and 3.5 as well @g-as

## 4.0.0 (2020-08-11)

- nothing changed yet

## 4.0.0a0 (2020-08-07)

- support isort >= 5 @bnavigator, @pkolbus

## 3.0.1 (2020-07-08)

- work around `FailedToLoadPlugin` exception by requiring `isort` 4.x. Likewise,
  pin the major version of all dependencies, to reduce risk of any future
  incompatibilities @pkolbus

## 3.0.0 (2020-04-15)

- let `isort` search the configuration, rather than `flake8-isort` try to find it @jnns

## 2.9.1 (2020-03-28)

- fix flake8 warning @sobolevn

## 2.9.0 (2020-03-16)

- add ``python3.8`` support @sobolevn

## 2.8.0 (2019-12-05)

- look for isort configuration on `.flake8` files as well @JohnHBrock

- document how to install `flake8-isort` on conda @marcelotrevisani

- look for isort configuration on `pyproject.toml` files as well @sanjioh

## 2.7.0 (2019-03-19)

- improve the README @barbossa

- fix isort output when pipes are used @maerteijn

## 2.6.0 (2018-12-01)

- use pytest to run tests @gforcada

- new error code I005 isort foundan unexpected missing import @charettes

- add `isort_show_traceback` option to show verbose multi-line output
  from `isort`, turned off by default @sobolevn

## 2.5 (2018-03-15)

- Now requires isort >= 4.3.0 @jleclanche

## 2.4 (2018-02-25)

- fix input handling with flake8's --stdin-display-name, and simplify it @blueyed

- remove flake8-polyfill dependency.  flake8 >= 3.2.1 is required already, and
  stdin is not read directly anymore @blueyed

## 2.3 (2017-12-22)

- fix typo @paltman

- add tox.ini and .editorconfig to config search @cas--

- make this plugin compatible with flake8 hook.
  As the hook copies the files out of tree,
  flake8-isort never finds the correct configuration @jaysonsantos

## 2.2.2 (2017-08-19)

- workaround for isort bug when skipping files @danpalmer

## 2.2.1 (2017-05-12)

- release as universal wheel @gforcada

## 2.2 (2017-03-26)

- support flake8 git hook @sergio-alonso

- support python 3.6 @gforcada

- search configuration on home folder @gforcada

## 2.1.3 (2016-11-25)

- fix yet another corner case @gforcada

## 2.1.2 (2016-11-25)

- fix another corner case: ignored files @cas--

## 2.1.1 (2016-11-25)

- fix corner cases of isort: newlines and grouped imports @cas--

## 2.1.0 (2016-11-24)

- show the exact line and kind of error,
  rather than a generic message @cas--

## 2.0.3 (2016-11-22)

- update trove classifiers @gforcada

## 2.0.2 (2016-11-22)

- add flake8 classifier @sigmavirus24

- require flake8 3.2.1.
  flake8 series 3.1.x and 3.2.0 where not reporting flake8-isort errors @gforcada

- test on pypy and pypy3 @gforcada

- fix tests and formatting @gforcada

## 2.0.1 (2016-09-22)

- fix standard input processing @carljm

## 2.0 (2016-09-14)

- Refactor code to handle flake8 version 3 @danpalmer

- require flake8 version 3.0 @gforcada

## 1.3 (2016-06-20)

- Make error messages clearer @do3cc

- use either pep8 or pycodestyle (new name for pep8) [Maxim Novikov]

- fix coveralls @gforcada

## 1.2 (2016-03-05)

- Allow stdin processing, this way text editor can pass input to flake8 @mjacksonw

## 1.1.1 (2016-02-16)

- silence isort messages @gforcada

- improve wording @gforcada

## 1.1 (2016-02-16)

- Check for isort configuration on setup.cfg as well @plumdog

## 1.0 (2015-12-16)

- check for an isort configuration file @gforcada

## 0.2 (2015-09-14)

- fix entry point @gforcada

## 0.1.post0 (2015-09-13)

- release wheels as well @gforcada

## 0.1 (2015-09-13)

- initial release @gforcada

- add all boilerplate files @gforcada

- create the flake8 plugin per se @gforcada
