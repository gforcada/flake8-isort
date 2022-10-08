.. -*- coding: utf-8 -*-

.. image:: https://github.com/gforcada/flake8-isort/actions/workflows/testing.yml/badge.svg?branch=master
   :target: https://github.com/gforcada/flake8-isort/actions/workflows/testing.yml

.. image:: https://coveralls.io/repos/gforcada/flake8-isort/badge.svg?branch=master
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

Install with conda::

    $ conda install -c conda-forge flake8-isort


Configuration
-------------
If using the `select` `option from flake8`_ be sure to enable the `I` category as well, see below for the specific error codes reported by `flake8-isort`.

Error codes
-----------
+------------+-----------------------------------------------------------+
| Error code | Description                                               |
+============+===========================================================+
| I001       | isort found an import in the wrong position               |
+------------+-----------------------------------------------------------+
| I002       | no configuration found (.isort.cfg or [isort] in configs) |
+------------+-----------------------------------------------------------+
| I003       | isort expected 1 blank line in imports, found 0           |
+------------+-----------------------------------------------------------+
| I004       | isort found an unexpected blank line in imports           |
+------------+-----------------------------------------------------------+
| I005       | isort found an unexpected missing import                  |
+------------+-----------------------------------------------------------+

Requirements
------------
- Python 3.7, 3.8, 3.9, 3.10 and pypy3
- flake8
- isort

Relation to flake8-import-order
-------------------------------

As an alternative to this flake8 plugin, there's `flake8-import-order`_ that could be worth checking out. In contrast to this plugin that defers all logic to isort, the flake8-import-order comes bundled with it's own logic.

flake8-import-order comes with a few predefined set of styles meanwhile this plugin can be customized a bit more. But the biggest difference could lie in that flake8-isort actually has the corresponding sorting engine isort that can sort the import orders of your existing python files. Meanwhile flake8-import-order has no such corresponding tool, hence big existing projects who want to adopt either would get a more automized experience choosing flake8-isort.

License
-------
GPL 2.0

.. _`isort`: https://pypi.python.org/pypi/isort
.. _`isort documentation`: https://pycqa.github.io/isort/docs/configuration/options.html
.. _`flake8-import-order`: https://pypi.python.org/pypi/flake8-import-order
.. _`option from flake8`: http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-select
