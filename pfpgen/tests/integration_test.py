#
# pfpgen: Code generation tool for creating models in the PFPSim Framework
#
# Copyright (C) 2016 Concordia Univ., Montreal
#     Samar Abdi
#     Umair Aftab
#     Gordon Bailey
#     Faras Dewal
#     Shafigh Parsazad
#     Eric Tremblay
#
# Copyright (C) 2016 Ericsson
#     Bochra Boughzala
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import unittest
import subprocess
import os
import inspect

# Get the path to this file, since test-cases are relative to it.
# http://stackoverflow.com/a/31867043/1084754
TEST_ROOT   = os.path.dirname(
                os.path.abspath(
                  inspect.getfile(inspect.currentframe()))) + "/integration/"

# http://stackoverflow.com/a/13197763/1084754
class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class Integration(unittest.TestCase):
    def test_main_no_args(self):
        """When run with no args, should output usage and exit"""
        p = subprocess.Popen(['pfpgen'],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        stdout, stderr = p.communicate()

        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(stdout, b"")
        # Error message changes between versions so we'll do a poor-man's startswith
        self.assertEqual(stderr[:13], b"usage: pfpgen")

    def test_nonexistant_file(self):
        """When run with no args, should output usage and exit"""
        fname = b"nonexistent-file.fad"
        p = subprocess.Popen(['pfpgen',fname],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        stdout, stderr = p.communicate()

        self.assertNotEqual(p.returncode, 0)
        self.assertEqual(stdout, b"")
        self.assertEqual(stderr, b"error: file '" + fname + b"' not found")

    def test_malformed_file(self):
        """When run with incorrect files, should output clean errors"""
        for f, error in (('yoda.fad', b"Line 1: Unexpected end of input\nPE top(\"yoda.cfg\"){\n                  ^\n"),
                         ('npu.fad',  b"Line 372: Unexpected token PE\nPE top(\"TopConfig.cfg\") {\n^\n"),):
            fname = TEST_ROOT + f
            p = subprocess.Popen(['pfpgen',fname],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

            stdout, stderr = p.communicate()

            self.assertNotEqual(p.returncode, 0)
            self.assertEqual(stdout, b"")
            self.assertEqual(stderr, error)

    def test_correct_file(self):
        basename = "SystemLevelTests"
        fadfile  = basename + ".fad"
        fname    = TEST_ROOT + fadfile
        with cd(TEST_ROOT):
            retcode = subprocess.call(['pfpgen',fname])

            self.assertEqual(retcode, 0)

            self.assertTrue(os.path.isdir(basename))
            self.assertTrue(os.path.isdir(basename + "/build"))

            with cd(basename + "/build"):
                self.assertEqual(0, subprocess.call(["cmake","../src"]))
                self.assertTrue(os.path.isfile("Makefile"))
                self.assertEqual(0, subprocess.call(["make"]))
                self.assertTrue(os.path.isfile(basename + "-sim"))
                self.assertEqual(0, subprocess.call(["./"+basename + "-sim"]))

            # remove all generated files
            self.assertEqual(0, subprocess.call(["git", "clean", "-dxf"]))




