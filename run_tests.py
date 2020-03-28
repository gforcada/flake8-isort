# -*- coding: utf-8 -*-
from flake8.main import application
from flake8_isort import Flake8Isort
from tempfile import mkdtemp
from testfixtures import OutputCapture

import collections
import os
import unittest


class TestFlake8Isort(unittest.TestCase):

    def _given_a_file_in_test_dir(self, contents, isort_config):
        test_dir = os.path.realpath(mkdtemp())
        file_path = os.path.join(test_dir, 'test.py')
        isort_path = os.path.join(test_dir, '.isort.cfg')
        with open(file_path, 'w') as a_file:
            a_file.write(contents)

        with open(isort_path, 'w') as a_file:
            a_file.write('[settings]\n')
            a_file.write(isort_config)

        return (file_path, contents)

    def test_sorted_correctly_alpha(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import path\n'
            '\n'
            'import os\n',
            isort_config='force_single_line=True\nforce_alphabetical_sort=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_sorted_correctly_default(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'import os\n'
            'from sys import path\n',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_with_eof_blank_lines(self):
        """Pass with eof blank line as flake8 will flag them"""
        (file_path, lines) = self._given_a_file_in_test_dir(
            'import os\n'
            'from sys import path\n'
            '\n'
            '\n'
            '   \n',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_imports_requires_blank_line(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from __future__ import division\n'
            'import threading\n'
            'from sys import pid\n',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I003 '))

    def test_isortcfg_skip_file(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'skipped_file',
            isort_config='skip=test.py'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_file_skipped_with_comment(self):
        # Note: files skipped in this way are not marked as
        # "skipped" by isort <= 4.2.15, so we handle them in a
        # different code path and test to ensure they also work.
        (file_path, lines) = self._given_a_file_in_test_dir(
            '# isort:skip_file',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_imports_unexpected_blank_line(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from __future__ import division\n'
            '\n'
            'import threading\n'
            '\n'
            'from sys import pid\n',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 4)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I004 '))

    def test_sorted_incorrectly_multiple(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from __future__ import division\n'
            'import os\n'
            'from sys import pid\n'
            'import threading\n'
            '\n'
            'import isort\n'
            '\n\n\n'
            'def func()\n',
            isort_config=''
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
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I001 '))

    def test_empty_file(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            '\n\n',
            isort_config=''
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_wrapped_imports(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from deluge.common import (fdate, fpcnt, fpeer, fsize, fspeed,\n'
            '                           ftime, get_path_size, is_infohash,\n'
            '                           is_ip, is_magnet, is_url)\n',
            isort_config='wrap_length=65'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_force_single_line_imports(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from plone.app.testing import applyProfile\n'
            'from plone.app.testing import FunctionalTesting\n',
            isort_config='force_alphabetical_sort=True\nforce_single_line=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_missing_add_imports(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'import os',
            isort_config='add_imports=from __future__ import unicode_literals'
        )
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
        # _given_a_file_in_test_dir already creates an .isort.cfg file
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )

        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I001 '))

    def test_isortcfg_not_found(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )
        # remove the .isort.cfg file
        isortcfg_path = file_path.split('/')[: -1]
        isortcfg_path = '{0}/.isort.cfg'.format('/'.join(isortcfg_path))
        os.remove(isortcfg_path)

        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            checker.search_current = False
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 0)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I002 '))

    def test_default_option(self):
        """By default a config file (.isort.cfg) is expected"""
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading\n',
            isort_config='force_single_line=True'
        )
        with OutputCapture():
            app = application.Application()
            app.run([file_path, ])
            self.assertTrue(Flake8Isort.config_file)

    def test_config_file(self):
        """Check that one can force to not look for a config file"""
        (file_path, lines) = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading\n',
            isort_config='force_single_line=True'
        )
        with OutputCapture():
            app = application.Application()
            app.run(['--no-isort-config', file_path, ])
            self.assertFalse(Flake8Isort.config_file)

    def test_isort_formatted_output(self):
        options = collections.namedtuple(
            'Options', [
                'no_isort_config',
                'isort_show_traceback',
                'stdin_display_name'
            ]
        )

        (file_path, lines) = self._given_a_file_in_test_dir(
            'from __future__ import division\n'
            'import os\n'
            'from sys import pid\n',
            isort_config=''
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

    def test_isort_uses_pyproject_toml_if_available(self):
        (file_path, lines) = self._given_a_file_in_test_dir(
            'import os\n'
            'from sys import path\n',
            isort_config=''
        )

        pyproject_toml_path = os.path.join(
            os.path.dirname(file_path), 'pyproject.toml',
        )
        with open(pyproject_toml_path, 'w') as f:
            f.write('[tool.isort]\nlines_between_types=1')

        with OutputCapture():
            checker = Flake8Isort(None, file_path, lines)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 2)
            self.assertEqual(ret[0][1], 0)
            self.assertTrue(ret[0][2].startswith('I003 '))
