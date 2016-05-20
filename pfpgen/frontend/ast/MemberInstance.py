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

class MemberInstance(AstNode):
    def __init__(self, name, lineno, config_path=None):
        super(MemberInstance, self).__init__(lineno)
        self.name = name
        self.config_path = config_path
        self._is_array = False
        self._array_size = None

    def __str__(self):

        s = (self.__class__.__name__ + ' ' + self.name)

        if self.config_path is not None:
            s += ' (' + self.config_path + ')'

        if self._is_array:
            if self._array_size is None:
                s += '[unspecified]'
            else:
                s += '[%d]' % self._array_size

        return s

    def set_array_size(self, size):
        self._is_array   = True
        self._array_size = size

    def is_array(self):
        return self._is_array

    def array_size(self):
        return self._array_size
