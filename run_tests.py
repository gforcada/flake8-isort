# -*- coding: utf-8 -*-
from flake8.main import application
from flake8_isort import Flake8Isort
from tempfile import mkdtemp
from testfixtures import OutputCapture

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
            a_file.write('[settings]')
            a_file.write(isort_config)

        return file_path

    def test_sorted_correctly(self):
        file_path = self._given_a_file_in_test_dir(
            'from sys import path\n'
            '\n'
            'import os'
            '\n',
            isort_config='force_single_line=True\nforce_alphabetical_sort=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path)
            ret = list(checker.run())
            self.assertEqual(ret, [])

    def test_sorted_incorrectly(self):
        file_path = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path)
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 0)
            self.assertEqual(ret[0][1], 0)
            self.assertIn(
                'I001 ',
                ret[0][2],
            )

    def test_isortcfg_found(self):
        # _given_a_file_in_test_dir already creates an .isort.cfg file
        file_path = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )
        with OutputCapture():
            checker = Flake8Isort(None, file_path)
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 0)
            self.assertEqual(ret[0][1], 0)
            self.assertIn(
                'I001 ',
                ret[0][2],
            )

    def test_isortcfg_not_found(self):
        file_path = self._given_a_file_in_test_dir(
            'from sys import pid\n'
            'import threading',
            isort_config='force_single_line=True'
        )
        # remove the .isort.cfg file
        isortcfg_path = file_path.split('/')[: -1]
        isortcfg_path = '{0}/.isort.cfg'.format('/'.join(isortcfg_path))
        os.remove(isortcfg_path)

        with OutputCapture():
            checker = Flake8Isort(None, file_path)
            checker.config_file = True
            ret = list(checker.run())
            self.assertEqual(len(ret), 1)
            self.assertEqual(ret[0][0], 0)
            self.assertEqual(ret[0][1], 0)
            self.assertIn(
                'I002 ',
                ret[0][2],
            )

    def test_default_option(self):
        """By default a config file (.isort.cfg) is expected"""
        app = application.Application()
        app.run([])
        self.assertTrue(Flake8Isort.config_file)

    def test_config_file(self):
        """Check that one can force to not look for a config file"""
        app = application.Application()
        app.run(['', '--no-isort-config'])
        self.assertFalse(Flake8Isort.config_file)


if __name__ == '__main__':
    unittest.main()
