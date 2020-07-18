"""unit tests for flake8-isort

the test should pass with both isort 4 and isort 5
"""

import collections
import os
import pytest

from flake8_isort import Flake8Isort


def write_python_file(tmpdir, content):
    file_path = os.path.join(str(tmpdir), 'test.py')
    with open(file_path, 'w') as python_file:
        python_file.write(content)
    return (file_path, content)


def write_isort_cfg(tmpdir, content):
    content = '[settings]\n' + content
    write_config_file(tmpdir, '.isort.cfg', content)


def write_setup_cfg(tmpdir, content):
    content = '[isort]\n' + content
    write_config_file(tmpdir, 'setup.cfg', content)


def write_tox_ini(tmpdir, content):
    content = '[isort]\n' + content
    write_config_file(tmpdir, 'tox.ini', content)


def write_pyproject_toml(tmpdir, content):
    content = '[tool.isort]\n' + content
    write_config_file(tmpdir, 'pyproject.toml', content)


def write_config_file(tmpdir, filename, content):
    file_path = os.path.join(str(tmpdir), filename)
    with open(file_path, 'w') as config_file:
        config_file.write(content)


def check_isort_ret(ret, ref):
    """Sort the return by (line, errortype) and compare it to the reference"""
    assert len(ret) == len(ref)
    for ret_i, ref_i in zip(sorted(ret, key=lambda x: (x[0], x[2])), ref):
        assert ret_i[:2] == ref_i[:2]
        assert ret_i[2].startswith(ref_i[2])


testcases = [
    {'name': 'sorted_correctly_default',
     'code': ('import os\n'
              'from sys import path\n'),
     'ref': []},
    {'name': 'sorted_correctly_alpha',
     'config': 'force_single_line=True\n'
               'force_alphabetical_sort=True\n',
     'code': 'from sys import path\n'
             '\n'
             'import os\n',
     'ref': []},
    {'name': 'eof_blank_lines',
     'code': 'import os\n'
             'from sys import path\n'
             '\n'
             '\n'
             '   \n',
     'ref': []},
    {'name': 'imports_requires_blank_line',
     'code': 'from __future__ import division\n'
             'import threading\n'
             'from sys import pid\n',
     'ref': [(2, 0, 'I003 ')]},
    {'name': 'isortcfg_skip_file',
     'config': 'skip=test.py',
     'code': 'skipped_file',
     'ref': []},
    {'name': 'file_skipped_with_comment',
     'code': '# isort:skip_file',
     'ref': []},
    {'name': 'imports_unexpected_blank_line',
     'code': 'from __future__ import division\n'
             '\n'
             'import threading\n'
             '\n'
             'from sys import pid\n',
     'ref': [(4, 0, 'I004 ')]},
    {'name': 'sorted_incorrectly_multiple',
     'code': 'from __future__ import division\n'
             'import os\n'
             'from sys import pid\n'
             'import threading\n'
             '\n'
             'import isort\n'
             '\n\n\n'
             'def func()\n',
     'ref': [(2, 0, 'I003 '),
             (4, 0, 'I001 '),
             (9, 0, 'I004 ')]},
    {'name': 'sorted_incorrectly',
     'config': 'force_single_line=True',
     'code': 'from sys import pid\n'
             'import threading',
     'ref': [(2, 0, 'I001 ')]},
    {'name': 'empty_file',
     'code': '\n\n',
     'ref': []},
    {'name': 'wrapped_imports',
     'config': 'wrap_length=65',
     'code': 'from deluge.common import (fdate, fpcnt, fpeer, fsize, fspeed,\n'
             '                           ftime, get_path_size, is_infohash,\n'
             '                           is_ip, is_magnet, is_url)\n',
     'ref': []},
    {'name': 'force_single_line_imports',
     'config': 'force_alphabetical_sort=True\n'
               'force_single_line=True',
     'code': 'from plone.app.testing import applyProfile\n'
             'from plone.app.testing import FunctionalTesting\n',
     'ref': []},
    {'name': 'missing_add_imports',
     'config': 'add_imports=from __future__ import unicode_literals',
     'code': 'import os\n',
     'ref': [(1, 0, 'I003'),
             (1, 0, 'I005')]},
]


@pytest.mark.parametrize('mode', ["file", "code_string"])
@pytest.mark.parametrize('testcase', testcases,
                         ids=[t['name'] for t in testcases])
def test_flake8_isort(tmpdir, testcase, mode):
    """Test the code examples in files and directly from string"""
    with tmpdir.as_cwd():
        if 'config' in testcase:
            write_isort_cfg(tmpdir, testcase['config'])
        if mode == "file":
            (file_path, lines) = write_python_file(tmpdir, testcase['code'])
            checker = Flake8Isort(None, file_path, lines)
        elif mode == "code_string":
            checker = Flake8Isort(None, None, testcase['code'])
        else:
            raise RuntimeError("invalid mode")
        ret = list(checker.run())
        check_isort_ret(ret, testcase['ref'])


def test_isortcfg_found(tmpdir):
    (file_path, lines) = write_python_file(
        tmpdir,
        'from sys import pid\n'
        'import threading',
    )
    write_isort_cfg(tmpdir, 'force_single_line=True')
    checker = Flake8Isort(None, file_path, lines)
    checker.config_file = True
    ret = list(checker.run())
    check_isort_ret(ret, [(2, 0, 'I001 ')])


def test_isortcfg_not_found(tmpdir):
    (file_path, lines) = write_python_file(
        tmpdir,
        'from sys import pid, path'
    )
    checker = Flake8Isort(None, file_path, lines)
    checker.search_current = False
    checker.config_file = True
    ret = list(checker.run())
    check_isort_ret(ret, [(1, 0, 'I001 ')])


def test_isort_formatted_output(tmpdir):
    options = collections.namedtuple(
        'Options', [
            'no_isort_config',
            'isort_show_traceback',
            'stdin_display_name'
        ]
    )

    (file_path, lines) = write_python_file(
        tmpdir,
        'from __future__ import division\n'
        'import os\n'
        'from sys import pid\n',
    )

    diff = ' from __future__ import division\n+\n import os'

    checker = Flake8Isort(None, file_path, lines)
    checker.parse_options(options(None, True, 'stdin'))
    ret = list(checker.run())
    assert len(ret) == 1
    assert ret[0][0] == 2
    assert ret[0][1] == 0
    assert diff in ret[0][2]


@pytest.mark.parametrize(
    'method_to_write_config',
    [write_isort_cfg, write_setup_cfg, write_tox_ini, write_pyproject_toml])
def test_if_config_file_is_used(tmpdir, method_to_write_config):
    (file_path, lines) = write_python_file(
        tmpdir,
        'import os\n'
        'from sys import path\n',
    )
    method_to_write_config(tmpdir, 'lines_between_types=1')

    checker = Flake8Isort(None, file_path, lines)
    ret = list(checker.run())
    check_isort_ret(ret, [(2, 0, 'I003 ')])
