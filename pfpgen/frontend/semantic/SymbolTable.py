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

from .SemanticError import SemanticError

class SymbolTable(object):
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
        self.n_errors = 0

    def __getitem__(self, item):
        if item in self.symbols:
            return self.symbols[item]
        elif self.parent is not None:
            return self.parent[item]
        else:
            raise SemanticError("Unknown object " + str(item))

    # For function calls and stuff like that proxy it through to the
    # underlying dictionary
    def __getattr__(self, attr):
        return getattr(self.symbols, attr)

    # We "override" update to first check that there are no duplicated
    # keys. We then use map.update as usual, since I assume it's faster
    # Than using __setitem__ in a loop.
    def update(self, other):
        for k in other.keys():
            if k in self.symbols:
                raise SemanticError("Duplicate definition of %s" % str(k))

        self.symbols.update(other)

    def __setitem__(self, item, value):
        if item in self.symbols:
            raise SemanticError("Duplicate definition of %s" % str(item))
        else:
            self.symbols[item] = value

    def debug_print(self):
        for k, v in self.symbols.items():
            v.debug_print()

    def get_all(self):
        return self.symbols.values()
