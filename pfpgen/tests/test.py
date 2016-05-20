#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import os
import inspect
import re
import keyword

import logging

from ..frontend          import compiler as c
from ..frontend.imports  import ImportManager

log = logging.getLogger('fad')

# Get the path to this file, since test-cases are relative to it.
# http://stackoverflow.com/a/31867043/1084754
TEST_ROOT   = os.path.dirname(
                os.path.abspath(
                  inspect.getfile(inspect.currentframe()))) + "/test-cases/"
TEST_SUFFIX = '.test'

SYNTAX_ERROR   = 'Syntax Error'
SEMANTIC_ERROR = 'Semantic Error'
SUCCESS        = 'Success'

def _is_valid_identifier(s):
    "Check if a string is a valid python identifier"
    # http://stackoverflow.com/a/12700971
    # Regex that it has the right form, then make sure
    # it is not a keyword or overriding a builtin

    if not re.match('^[A-Za-z_][A-Za-z_0-9]*$', s):
        log.warning("Identifier {} contains invalid characters".format(s))
        return False

    if keyword.iskeyword(s) or s in ('True', 'False', 'None'):
        log.warning("Identifier {} is a python keyword".format(s))
        return False

    if s in dir(__builtins__):
        log.warning("Identifier {} is a python builtin".format(s))
        return False

    return True

def build_test_method(name, description, fad_program, expected):
    def test(self):
        compiler = c.Compiler(ImportManager(
            [TEST_ROOT + "modules/user/", TEST_ROOT + "modules/user2"],
            [TEST_ROOT + "modules/sys/",  TEST_ROOT + "modules/sys2"] ))

        hlir = compiler.compile_to_hlir(fad_program, "test")

        if hlir is None:
            if compiler.result == c.SYNTAX_ERROR:
                self.assertEqual(expected, SYNTAX_ERROR)
            elif compiler.result == c.SEMANTIC_ERROR:
                self.assertEqual(expected, SEMANTIC_ERROR)
            else:
                self.assertEqual(expected, "Unknown Problem")
        else:
            self.assertEqual(expected, SUCCESS)


        # TODO TODO TODO
        #genobj = fadgen(hlir)
        #genobj.logginglevel('WARNING')
        #genobj.rungenerator()


    # Programmatically change the name and docstring of the
    # instance of the member function and return it
    test.__name__ = 'test_' + name
    test.__doc__  = description
    return test



def create_test_methods(f):
    with open(TEST_ROOT + f) as data:
        lines = data.readlines()
        i     = 0

        while i < len(lines):

            name = lines[i].strip()
            if not _is_valid_identifier(name):
                return
            i += 1

            description = lines[i].strip()
            i += 1

            if lines[i].strip() != '':
                log.warning("Expecting blank line after description")
                return
            i += 1

            fad_program = ""
            while i < len(lines) and not lines[i].startswith('%'):
                fad_program += lines[i]
                i += 1

            if i >= len(lines):
                log.warning("Unexpected EOF: Expecting terminating line (line starting with '%')")
                return

            assert(lines[i].startswith('%'))
            expected = lines[i][1:].strip()

            try:
                expected = {
                        'SYN':SYNTAX_ERROR,
                        'SEM':SEMANTIC_ERROR,
                        'SUC':SUCCESS }[expected]
            except KeyError:
                log.warning("Unknown expected result type {}. (Should be SYN, SEM, or SUC)".format(expected))
                return

            yield build_test_method(name, description, fad_program, expected)
            i += 1
            while i < len(lines) and lines[i].strip() == '':
                i += 1

def create_test_class(f):
    # http://stackoverflow.com/a/4859312
    #
    # We can add things to this dictionary to
    # create new entities at global scope
    _module = globals()

    assert(f.endswith(TEST_SUFFIX))
    assert(len(f) > len(TEST_SUFFIX))
    name = f[:-len(TEST_SUFFIX)]

    methods = {}
    for method in create_test_methods(f):
        methods[method.__name__] = method

    cls = type(name, (unittest.TestCase,), methods)
    _module[name] = cls
    return cls

suite  = unittest.TestSuite()
loader = unittest.TestLoader()

for f in os.listdir(TEST_ROOT):
    if f.endswith(TEST_SUFFIX) and len(f) > len(TEST_SUFFIX):
        cls = create_test_class(f)
        suite.addTests(loader.loadTestsFromTestCase(cls))

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=1, descriptions=True, buffer=True).run(suite)
