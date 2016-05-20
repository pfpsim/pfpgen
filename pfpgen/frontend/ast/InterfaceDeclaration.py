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

from .AstNode import AstNode

from ..semantic.hlir import Interface

class InterfaceDeclaration(AstNode):
    def __init__(self, names, lineno):
        super(InterfaceDeclaration, self).__init__(lineno)
        self.names = names

    def __str__(self):
            return (self.__class__.__name__ +
                '<' + ', '.join(self.names) + '>')

    def _analyze_pass_1(self, symbol_table):
        for name in self.names:
            symbol_table[name.name] = Interface(name.name, name.config_path)


    def _analyze_pass_2(self, symbol_table):
        pass # Nothing more to do
