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

from ..semantic import SemanticError
from .AstNode import AstNode

class ImportStatement(AstNode):
    def __init__(self, module_spec, import_manager, lineno):
        super(ImportStatement, self).__init__(lineno)
        self.module_spec = module_spec
        # This is a seinfeld reference ... I'm sorry :P
        # http://pkmeco.com/seinfeld/cadillac.htm
        self.art_vandelay = import_manager

    def __str__(self):
        return (self.__class__.__name__ + '/'.join(self.module_spec))

    # In pass 1 we need to *fully* process the included file. Then we need to
    # drag out all of its symbols into the current scope (which is the global
    # scope)
    def _analyze_pass_1(self, symbol_table):
        symbols = self.art_vandelay.import_module(self.module_spec)

        symbol_table.update(symbols)



    def _analyze_pass_2(self, context):
        pass
