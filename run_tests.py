# -*- coding: utf-8 -*-
from flake8.main import application
from flake8_isort import Flake8Isort
from tempfile import mkdtemp
from testfixtures import OutputCapture

import collections
import os
import unittest


class TestFlake8Isort(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.realpath(mkdtemp())

    def write_python_file(self, content):
        file_path = os.path.join(self.test_dir, 'test.py')
        with open(file_path, 'w') as python_file:
            python_file.write(content)
        return (file_path, content)

    def write_isort_cfg(self, content):
        content = '[settings]\n' + content
        self.write_config_file('.isort.cfg', content)

    def write_setup_cfg(self, content):
        content = '[isort]\n' + content
        self.write_config_file('setup.cfg', content)

    def write_tox_ini(self, content):
        content = '[isort]\n' + content
        self.write_config_file('tox.ini', content)

    def write_pyproject_toml(self, content):
        content = '[tool.isort]\n' + content
        self.write_config_file('pyproject.toml', content)

    def write_config_file(self, name, content):
        file_path = os.path.join(self.test_dir, name)
        with open(file_path, 'w') as config_file:
            config_file.write(content)

    def test_sorted_correctly_alpha(self):
        (file_path, lines) = self.write_python_file(
            'from sys import path\n'
            '\n'
            'import os\n',
        )
        self.write_isort_cfg('force_single_line=True\nforce_alphabetical_sort=True')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_sorted_correctly_default(self):
        (file_path, lines) = self.write_python_file(
            'import os\n'
            'from sys import path\n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_with_eof_blank_lines(self):
        """Pass with eof blank line as flake8 will flag them"""
        (file_path, lines) = self.write_python_file(
            'import os\n'
            'from sys import path\n'
            '\n'
            '\n'
            '   \n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_imports_requires_blank_line(self):
        (file_path, lines) = self.write_python_file(
            'from __future__ import division\n'
            'import threading\n'
            'from sys import pid\n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I003 '))

    def test_isortcfg_skip_file(self):
        (file_path, lines) = self.write_python_file(
            'skipped_file',
        )
        self.write_isort_cfg('skip=test.py')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_file_skipped_with_comment(self):
        # Note: files skipped in this way are not marked as
        # "skipped" by isort <= 4.2.15, so we handle them in a
        # different code path and test to ensure they also work.
        (file_path, lines) = self.write_python_file(
            '# isort:skip_file',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_imports_unexpected_blank_line(self):
        (file_path, lines) = self.write_python_file(
            'from __future__ import division\n'
            '\n'
            'import threading\n'
            '\n'
            'from sys import pid\n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 4)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I004 '))

    def test_sorted_incorrectly_multiple(self):
        (file_path, lines) = self.write_python_file(
            'from __future__ import division\n'
            'import os\n'
            'from sys import pid\n'
            'import threading\n'
            '\n'
            'import isort\n'
            '\n\n\n'
            'def func()\n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 3)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I003 '))
            self.assertEqual(ret[1][0], 4)
            self.assertEqual(ret[1][1], 0)
            self.assertTrue(ret[1][2].startswith('I001 '))
            self.assertEqual(ret[2][0], 9)
            self.assertEqual(ret[2][1], 0)
            self.assertTrue(ret[2][2].startswith('I004 '))

    def test_sorted_incorrectly(self):
        (file_path, lines) = self.write_python_file(
            'from sys import pid\n'
            'import threading',
        )
        self.write_isort_cfg('force_single_line=True')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I001 '))

    def test_empty_file(self):
        (file_path, lines) = self.write_python_file(
            '\n\n',
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_wrapped_imports(self):
        (file_path, lines) = self.write_python_file(
            'from deluge.common import (fdate, fpcnt, fpeer, fsize, fspeed,\n'
            '                           ftime, get_path_size, is_infohash,\n'
            '                           is_ip, is_magnet, is_url)\n',
        )
        self.write_isort_cfg('wrap_length=65')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_force_single_line_imports(self):
        (file_path, lines) = self.write_python_file(
            'from plone.app.testing import applyProfile\n'
            'from plone.app.testing import FunctionalTesting\n',
        )
        self.write_isort_cfg('force_alphabetical_sort=True\nforce_single_line=True')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_missing_add_imports(self):
        (file_path, lines) = self.write_python_file('import os')
        self.write_isort_cfg('add_imports=from __future__ import unicode_literals')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 2)
            self.assertEqual(ret[0][0], 1)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I005 '))
            self.assertEqual(ret[1][0], 1)
            self.assertEqual(ret[1][1], 0)
            self.assertTrue(ret[1][2].startswith('I003 '))

    def test_isortcfg_found(self):
        (file_path, lines) = self.write_python_file(
            'from sys import pid\n'
            'import threading',
        )
        self.write_isort_cfg('force_single_line=True')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I001 '))

    def test_isortcfg_not_found(self):
        (file_path, lines) = self.write_python_file('from sys import pid, path')
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            checker.search_current = False
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 1)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I001 '))

    def test_isort_formatted_output(self):
        options = collections.namedtuple(
            'Options', [
                'no_isort_config',
                'isort_show_traceback',
                'stdin_display_name'
            ]
        )

        (file_path, lines) = self.write_python_file(
            'from __future__ import division\n'
            'import os\n'
            'from sys import pid\n',
        )

        diff = ' from __future__ import division\n+\n import os'

        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            checker.parse_options(options(None, True, 'stdin'))
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertIn(diff, ret[0][2])

    def test_if_isort_cfg_is_used(self):
        self.check_if_config_file_is_used(self.write_isort_cfg)

    def test_if_setup_cfg_is_used(self):
        self.check_if_config_file_is_used(self.write_setup_cfg)

    def test_if_tox_ini_is_used(self):
        self.check_if_config_file_is_used(self.write_tox_ini)

    def test_if_pyproject_toml_is_used(self):
        self.check_if_config_file_is_used(self.write_pyproject_toml)

    def check_if_config_file_is_used(self, method_to_write_config):
        (file_path, lines) = self.write_python_file(
            'import os\n'
            'from sys import path\n',
        )
        method_to_write_config('lines_between_types=1')

        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I003 '))
