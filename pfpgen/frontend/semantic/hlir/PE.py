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

from ..SymbolTable import SymbolTable
from .Type import Type

class PE(SymbolTable, Type):
    def __init__(self, name, parent_symbol_table, config):
        SymbolTable.__init__(self, parent_symbol_table)
        Type.__init__(self, config)

        self.name            = name
        self.services        = []
        self.interfaces      = []
        self.pe_members      = []
        self.ce_members      = []
        self.bindings        = []
        self.service_members = []

    def __str__(self):
        return self.__class__.__name__ + " " + self.name

    def debug_print(self):
        s = "PE "

        s += self.name
        s += " implements " + ', '.join(map(str, self.services))
        s += "\n"

        for interface in self.interfaces:
            s += "  " + str(interface) + "\n"

        if len(self.interfaces) > 0:
            s += "\n"

        for ce in self.ce_members:
            s += "  " + str(ce) + "\n"

        if len(self.ce_members) > 0:
            s += "\n"

        for pe in self.pe_members:
            s += "  " + str(pe) + "\n"

        if len(self.pe_members) > 0:
            s += "\n"

        for binding in self.bindings:
            s += "  " + str(binding) + "\n"

        s += "END PE " + self.name

        print (s)
