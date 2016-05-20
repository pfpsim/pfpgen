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

import os

from .compiler import Compiler
from .semantic import SemanticError

# TODO
class Importer(object):
    def __init__(self, path, is_user_import):
        self.path = path
        self.user = is_user_import

    def __call__(self):
        pass

class ImportManager(object):
    def __init__(self, user_paths, sys_paths):

        def ensure_endswith_sep(path):
            if path.endswith(os.path.sep):
                return path
            else:
                return path + os.path.sep

        self.user_paths = map(ensure_endswith_sep, user_paths)
        self.sys_paths  = map(ensure_endswith_sep, sys_paths)

        self.imported_modules = set()

    def import_module(self, mod_path):
        # Resolve an import

        # First convert module path to filesystem path:
        #   this.is.an.example => this/is/an/example.fad
        path = os.path.sep.join(mod_path) + ".fad"

        # If we have already imported this module, then we don't need to (and shouldn't)
        # re-import it. We just short circuit out of it
        if path in self.imported_modules:
            # Return an empty dictionary, we don't need to add any new symbols
            return {}

        # Then we look in the user path for the specified module
        for prefix in self.user_paths:
            upath = prefix + path
            syms  = self.parse_module(upath)
            if syms is not None:
                self.imported_modules.add(path)
                return syms

        # Then we try to parse it as a system include
        for prefix in self.sys_paths:
            spath = prefix + path
            syms  = self.parse_module(spath)
            # TODO mark this as "do not generate"
            if syms is not None:
                self.imported_modules.add(path)
                return syms

        # If we didnt reaturn by this point, then it's not found so we'll
        # throw an erorr
        raise SemanticError("Module not found: {}".format(path))

    def parse_module(self, mod_path):
        if os.path.isfile(mod_path):
            compiler = Compiler(self)
            with open(mod_path) as mod_file:
                c = Compiler(self)
                syms = c.compile_to_symbols(mod_file.read())
                if syms is None:
                    raise SemanticError("Could not import module {}".format(mod_path))
                return syms
        else:
            return None
