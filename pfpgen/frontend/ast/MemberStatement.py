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

from ..semantic.hlir import Instance, TypeSpecifier, PE, CE, Interface, Service
from ..semantic.SemanticError import SemanticError
from .AstNode import AstNode

class MemberStatement(AstNode):
    def __init__(self, name, members, lineno):
        super(MemberStatement, self).__init__(lineno)
        self.name    = name
        self.members = members

    def __str__(self):
        return (self.__class__.__name__ +
            ' ' + self.name + '<' + ', '.join(map(str, self.members)) + '>')

    def _analyze_pass_1(self, context):
        type_obj = context[self.name]

        for member in self.members:
            member_type = TypeSpecifier(
                    type_obj,
                    member.is_array(),
                    member.array_size())
            context[member.name] = Instance(
                    member_type,
                    member.name,
                    member.config_path)

    def _analyze_pass_2(self, context):
        type = context[self.name]

        if   type.__class__ is PE:
            for member in self.members:
                context.pe_members.append(context[member.name])
        elif type.__class__ is CE:
            for member in self.members:
                context.ce_members.append(context[member.name])
        elif type.__class__ is Interface:
            for member in self.members:
                context.interfaces.append(context[member.name])
        elif type.__class__ is Service:
            for member in self.members:
                context.service_members.append(context[member.name])
        else:
            raise SemanticError(
                    "Cannot directly instantiate a " + type.__class__.__name__)
