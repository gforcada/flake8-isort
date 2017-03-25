.. -*- coding: utf-8 -*-

.. image:: https://travis-ci.org/gforcada/flake8-isort.svg?branch=master
   :target: https://travis-ci.org/gforcada/flake8-isort

.. image:: https://coveralls.io/repos/gforcada/flake8-isort/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/gforcada/flake8-isort?branch=master

Flake8 meet isort
=================
Use `isort`_ to check if the imports on your python files are sorted the way you expect.

Add an ``.isort.cfg`` to define how you want your imports sorted and run flake8 as you usually do.

See `isort documentation`_ for ``.isort.cfg`` available options.

Install
-------
Install with pip::

    $ pip install flake8-isort

Options
-------
Since version 1.0 a check for an ``.isort.cfg`` file is done,
since version 1.1 ``setup.cfg`` is also checked for an ``[isort]`` section.

This potentially avoids to lint a project that has no formal definition of how import should be sorted.

With either ``--no-isort-config`` command line switch,
or ``no-isort-config`` flake8 configuration option it can be disabled.

Requirements
------------
- Python 2.7, 3.5, 3.6, pypy or pypy3
- flake8
- isort

Relaion to flake8-import-order
------------------------------

As an alternative to this flake8 plugin, there's `flake8-import-order`_ that could be worth checking out. In contrast to this plugin that defers all logic to isort, the flake8-import-order comes bundled with it's own logic. 

flake8-import-order comes with a few predefined set of styles meanwhile this plugin can be customized a bit more. But the biggest difference could lie in that flake8-isort actually has the corresponding sorting engine isort that can sort the import orders of your existing python files. Meanwhile flake8-import-order has no such corresponding tool, hence big existing projects who want to adopt either would get a more automized experience choosing flake8-isort.

License
-------
GPL 2.0

.. _`isort`: https://pypi.python.org/pypi/isort
.. _`isort documentation`: https://github.com/timothycrosley/isort/wiki/isort-Settings
.. _`flake8-import-order`: https://pypi.python.org/pypi/flake8-import-order
