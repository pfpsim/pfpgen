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

class InstanceSpecifier(AstNode):

    class InstanceFragment(object):
        def __init__(self, name, array_index):
            self.name = name
            self.array_index = array_index
        def __str__(self):
            if self.array_index is None:
                return self.name
            else:
                return self.name + '[' + str(self.array_index) + ']'

    def __init__(self, name, lineno, array_index = None):
        super(InstanceSpecifier, self).__init__(lineno)
        self.entries = [ InstanceSpecifier.InstanceFragment(name, array_index) ]

    def __iter__(self):
        return self.entries.__iter__()

    def __len__(self):
        return self.entries.__len__()

    def __getitem__(self, index):
        return self.entries.__getitem__(index)

    def append(self, other):
        self.entries += other.entries

    def __str__(self):
        return (self.__class__.__name__ +
            ' ' +  '.'.join(map(str, self.entries)) )
