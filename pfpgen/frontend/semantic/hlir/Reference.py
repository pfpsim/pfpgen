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

from . import Instance
from ..SemanticError import SemanticError

class Subreference(object):
    def __init__(self, instance):
        self.instance = instance
        self.index    = None

    def clone(self):
        clone_val = Subreference(self.instance)
        clone_val.index = self.index
        return clone_val

    def is_array_reference(self):
        return self.index is not None

    def __str__(self):
        if self.index is None:
            return str(self.instance)
        else:
            return "%s[%d]" % (self.instance, self.index)

class Reference(object):
    def __init__(self, context, name=None):
        self.reference_list = []
        self.context        = context

        if name is not None:
            self.dot(name)

    def __getitem__(self,index):
        return self.reference_list.__getitem__(index)
    def __len__(self):
        return self.reference_list.__len__()
    def clone(self):
        copy                = Reference(self.context)
        copy.reference_list = list(map(Subreference.clone, self.reference_list))

        return copy

    def dot(self, name):
        if self.is_array():
            raise SemanticError("Non-array access to array type")

        inst = self.context[name]

        if inst.__class__ is not Instance:
            raise SemanticError("Cannot refer directly to a " + inst.__class__.__name__)

        self.reference_list.append(Subreference(inst))
        self.context = inst.type.base_type

    def index(self, i):
        if not self.is_array():
            raise SemanticError("Array access of non-array value " + self.reference_list[-1].instance.name)

        if self.array_size() is not None and self.array_size() <= i:
            raise SemanticError("Out of bounds array access")

        self.reference_list[-1].index = i

    def is_array(self):
        if len(self.reference_list) == 0:
            return False

        if self.reference_list[-1].index is not None:
            return False

        x = self.reference_list[-1].instance

        return self.reference_list[-1].instance.type.is_array

    def is_array_reference(self):
        if len(self.reference_list) == 0:
            return False

        return self.reference_list[-1].index is not None

    def array_size(self):
        return self.reference_list[-1].instance.type.array_size

    def get_base_type(self):
        if len(self.reference_list) > 0:
            return self.reference_list[-1].instance.type.base_type
        else:
            return None

    def get_parent(self):
        # Copy our reference list minus the topmost reference
        new_reflist = self.reference_list[:-1]

        # Create a new reference based off that new reference list
        newref = Reference(None)
        newref.reference_list = new_reflist
        newref.context = newref.get_base_type()

        return newref


    def __str__(self):
        return '.'.join(map(str, self.reference_list))
