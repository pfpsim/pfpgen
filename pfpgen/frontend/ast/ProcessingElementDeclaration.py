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

from ..semantic.hlir import PE, Service
from ..semantic.SemanticError import SemanticError
from .AstNode import AstNode

class ProcessingElementDeclaration(AstNode):
    def __init__(self, name, lineno, services=[]):
        super(ProcessingElementDeclaration, self).__init__(lineno)
        self.name        = name.name
        self.config_path = name.config_path
        self.services    = services
        self.statements  = []

    def set_statements(self, statements):
        self.statements = statements

    def __str__(self):
        return (self.__class__.__name__ + ' '
                + ', '.join(self.services) +
                ' ' + self.name + ':\n  ' + '\n  '.join(map(str, self.statements)))

    # First pass on the PE declaration puts it in the symbol table and
    # then passes over all its child statements in the context of the
    # parent
    def _analyze_pass_1(self, context):
        pe = PE(self.name, context, self.config_path)
        context[self.name] = pe

    # Here each statement adds itself to the parent (us)
    def _analyze_pass_2(self, context):
        pe = context[self.name]

        for service in self.services:
            s = context[service]
            if type(s) is not Service:
                raise SemanticError("PE may only implement Services, not " + s.__class__.__name__)
            pe.services.append(s)

        for statement in self.statements:
            statement.analyze_pass_1(pe)

        for statement in self.statements:
            statement.analyze_pass_2(pe)
