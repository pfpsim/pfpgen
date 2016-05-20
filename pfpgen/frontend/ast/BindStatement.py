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
from ..semantic.hlir import Reference, Binding
from .AstNode import AstNode

class BindStatement(AstNode):
    def __init__(self, source, destinations, lineno):
        super(BindStatement, self).__init__(lineno)
        self.source = source
        self.destinations = destinations

    def __str__(self):
        return (self.__class__.__name__ +
            ' ' + str(self.source) + ' -> ['
            + ', '.join(map(str, self.destinations)) + ']')

    def _analyze_pass_1(self, symbol_table):
        pass # nothing to do yet

    def _resolve_reference(self, ref, context):
        value = Reference(context, ref[0].name)
        if ref[0].array_index is not None:
            value.index(ref[0].array_index)

        for r in ref[1:]:
            value.dot(r.name)
            if r.array_index is not None:
                value.index(r.array_index)

        return value

    def _bind_array_src(self, src_ref, context):
        if not ( src_ref.array_size() == len(self.destinations)
        or src_ref.array_size() is None ):
            raise SemanticError(
                "Number of bind destinations (%d) must match source array size (%d)"
                % ( len(self.destinations), src_ref.array_size()))


        # TODO(gordon) Here we could implement the "Binding resolution pass"
        for i, dest in enumerate(self.destinations):
            dst_ref = self._resolve_reference(dest, context)
            src_ref_copy = src_ref.clone()
            src_ref_copy.index(i)
            context.bindings.append(Binding(src_ref_copy, dst_ref))


    def _bind_scalar_src(self, src_ref, context):
        if len(self.destinations) != 1:
            raise SemanticError(
                "Number of bind destinations (%d) must be 1 for non-array source"
                % (len(self.destinations,)))

        dst_ref = self._resolve_reference(self.destinations[0], context)
        context.bindings.append(Binding(src_ref, dst_ref))


    def _analyze_pass_2(self, context):
        src_ref = self._resolve_reference(self.source, context)

        if src_ref.is_array():
            self._bind_array_src(src_ref, context)
        else:
            self._bind_scalar_src(src_ref, context)
