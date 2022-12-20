"""unit tests for flake8-isort"""

import collections
import os
import textwrap
import pytest

from flake8_isort import Flake8Isort


def write_python_file(tmpdir, content):
    source = textwrap.dedent(content)
    file_path = os.path.join(str(tmpdir), 'test.py')
    with open(file_path, 'w') as python_file:
        python_file.write(source)
    return (file_path, source)


def write_isort_cfg(tmpdir, content):
    write_config_file(tmpdir, '.isort.cfg', 'settings', content)


def write_setup_cfg(tmpdir, content):
    write_config_file(tmpdir, 'setup.cfg', 'isort', content)


def write_tox_ini(tmpdir, content):
    write_config_file(tmpdir, 'tox.ini', 'isort', content)


def write_pyproject_toml(tmpdir, content):
    write_config_file(tmpdir, 'pyproject.toml', 'tool.isort', content)


def write_config_file(tmpdir, filename, header, content):
    source = f'[{header}]\n{textwrap.dedent(content)}'
    file_path = os.path.join(str(tmpdir), filename)
    with open(file_path, 'w') as config_file:
        config_file.write(source)


def check_isort(return_values, references):
    """Sort the return by (line, errortype) and compare it to the reference"""
    assert len(return_values) == len(references)
    for return_value, reference in zip(
        sorted(return_values, key=lambda x: (x[0], x[2])), references
    ):
        assert return_value[:2] == reference[:2]
        assert return_value[2].startswith(reference[2])


testcases = [
    {
        'name': 'sorted_correctly_default',
        'code': """
            import os
            from sys import path
            """,
        'reference': [],
    },
    {
        'name': 'sorted_correctly_alpha',
        'config': """
            force_single_line=True
            force_alphabetical_sort=True
            """,
        'code': """
            from sys import path

            import os
            """,
        'reference': [],
    },
    {
        'name': 'eof_blank_lines',
        'code': """
            import os
            from sys import path



               """,
        'reference': [],
    },
    {
        'name': 'imports_requires_blank_line',
        'code': """
            from __future__ import division
            import threading
            from sys import pid
            """,
        'reference': [(3, 0, 'I003 ')],
    },
    {
        'name': 'isortcfg_skip_file',
        'config': 'skip=test.py',
        'code': 'skipped_file',
        'reference': [],
    },
    {'name': 'file_skipped_with_comment', 'code': '# isort:skip_file', 'reference': []},
    {
        'name': 'imports_unexpected_blank_line',
        'code': """
            from __future__ import division

            import threading

            from sys import pid
            """,
        'reference': [(5, 0, 'I004 ')],
    },
    {
        'name': 'sorted_incorrectly_multiple',
        'code': """
            from __future__ import division
            import os
            from sys import pid
            import threading

            import isort



            def func(): ...
            """,
        'reference': [(3, 0, 'I003 '), (5, 0, 'I001 '), (10, 0, 'I004 ')],
    },
    {
        'name': 'sorted_incorrectly',
        'config': 'force_single_line=True',
        'code': """
            from sys import pid
            import threading
            """,
        'reference': [(3, 0, 'I001 ')],
    },
    {'name': 'empty_file', 'code': '\n\n', 'reference': []},
    {
        'name': 'wrapped_imports',
        'config': 'wrap_length=65',
        'code': """
            from deluge.common import (fdate, fpcnt, fpeer, fsize, fspeed,
                                       ftime, get_path_size, is_infohash,
                                       is_ip, is_magnet, is_url)
            """,
        'reference': [],
    },
    {
        'name': 'force_single_line_imports',
        'config': """
            force_alphabetical_sort=True
            force_single_line=True
            """,
        'code': """
            from plone.app.testing import applyProfile
            from plone.app.testing import FunctionalTesting
            """,
        'reference': [],
    },
    {
        'name': 'missing_add_imports',
        'config': 'add_imports=from __future__ import unicode_literals',
        'code': 'import os\n',
        'reference': [(1, 0, 'I003'), (1, 0, 'I005')],
    },
]


@pytest.mark.parametrize('mode', ['file', 'code_string'])
@pytest.mark.parametrize('testcase', testcases, ids=[t['name'] for t in testcases])
def test_flake8_isort(tmpdir, testcase, mode):
    """Test the code examples in files and directly from string"""
    with tmpdir.as_cwd():
        if 'config' in testcase:
            write_isort_cfg(tmpdir, testcase['config'])
        if mode == 'file':
            (file_path, lines) = write_python_file(tmpdir, testcase['code'])
            checker = Flake8Isort(None, file_path, lines)
        elif mode == 'code_string':
            source = textwrap.dedent(testcase['code'])
            checker = Flake8Isort(None, None, source)
        return_values = list(checker.run())
        check_isort(return_values, testcase['reference'])


def test_isortcfg_found(tmpdir):
    source = """
    from sys import pid
    import threading
    """
    (file_path, lines) = write_python_file(tmpdir, source)
    write_isort_cfg(tmpdir, 'force_single_line=True')
    checker = Flake8Isort(None, file_path, lines)
    checker.config_file = True
    ret = list(checker.run())
    check_isort(ret, [(3, 0, 'I001 ')])


def test_isortcfg_not_found(tmpdir):
    (file_path, lines) = write_python_file(tmpdir, 'from sys import pid, path')
    checker = Flake8Isort(None, file_path, lines)
    checker.search_current = False
    checker.config_file = True
    ret = list(checker.run())
    check_isort(ret, [(1, 0, 'I001 ')])


def test_isort_formatted_output(tmpdir):
    source = """
    from __future__ import division
    import os
    from sys import pid
    """
    options = collections.namedtuple(
        'Options',
        [
            'no_isort_config',
            'isort_show_traceback',
            'stdin_display_name',
            'isort_no_skip_gitignore',
        ],
    )

    (file_path, lines) = write_python_file(tmpdir, source)

    diff = ' from __future__ import division\n+\n import os'

    checker = Flake8Isort(None, file_path, lines)
    checker.parse_options(None, options(None, True, 'stdin', None), None)
    ret = list(checker.run())
    assert len(ret) == 1
    assert ret[0][0] == 3
    assert ret[0][1] == 0
    assert diff in ret[0][2]


@pytest.mark.parametrize(
    'method_to_write_config',
    [write_isort_cfg, write_setup_cfg, write_tox_ini, write_pyproject_toml],
)
def test_if_config_file_is_used(tmpdir, method_to_write_config):
    source = """
    import os
    from sys import path
    """
    (file_path, lines) = write_python_file(
        tmpdir,
        source,
    )
    method_to_write_config(tmpdir, 'lines_between_types=1')

    checker = Flake8Isort(None, file_path, lines)
    ret = list(checker.run())
    check_isort(ret, [(3, 0, 'I003 ')])


def test_flake8(tmpdir):
    from flake8.main import cli
    import sys

    (file_path, lines) = write_python_file(tmpdir, 'from sys import pid, path')

    sys.argv = sys.argv[:2]
    try:
        assert isinstance(cli.main(), int)
    except SystemExit:
        pass
