# Flake8 meet isort

Use [isort](https://pypi.org/project/isort) to check
if the imports on your python files are sorted the way you expect.

Add an `.isort.cfg` configuration file to define
how you want your imports sorted and run `flake8` as you usually do.

See [isort documentation](https://pycqa.github.io/isort/docs/configuration/options.html)
for `.isort.cfg` available options.

## Install

Install with pip:

```shell
pip install flake8-isort
```

Install with conda:

```shell
conda install -c conda-forge flake8-isort
```

## Configuration

If using the `select` [option from flake8](http://flake8.pycqa.org/en/latest/user/options.html#cmdoption-flake8-select)
be sure to enable the `I` category as well,
see below for the specific error codes reported by `flake8-isort`.

See `flake8 --help` for available `flake8-isort` options.

## Error codes

| Error code | Description                                               |
|------------|-----------------------------------------------------------|
| I001       | isort found an import in the wrong position               |
| I002       | no configuration found (.isort.cfg or [isort] in configs) |
| I003       | isort expected 1 blank line in imports, found 0           |
| I004       | isort found an unexpected blank line in imports           |
| I005       | isort found an unexpected missing import                  |

## Requirements

- Python 3.1+ and pypy3
- flake8
- isort

## Relation to flake8-import-order

As an alternative to this flake8 plugin, there's [flake8-import-order](https://pypi.org/project/flake8-import-order)
that could be worth checking out.
In contrast to this plugin that defers all logic to isort,
the flake8-import-order comes bundled with it's own logic.

`flake8-import-order` comes with a few predefined set of styles
meanwhile this plugin can be customized a bit more.
But the biggest difference could lie in that `flake8-isort`
actually has the corresponding sorting engine isort
that can sort the import orders of your existing python files.
Meanwhile `flake8-import-order` has no such corresponding tool.

## License

GPL 2.0
