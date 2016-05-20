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

from ..SemanticError import SemanticError

class TypeSpecifier:
    def __init__(self, type, is_array=False, array_size=None):
        self.base_type  = type
        self.is_array   = is_array
        self.array_size = array_size

    def __str__(self):
        if self.is_array:
            return "%s [%s]" % (
                    str(self.base_type), self.array_size if self.array_size is not None else "?")

        else:
            return str(self.base_type)

class Instance:
    def __init__(self, type, name, config_path=None):
        self.type        = type
        self.name        = name
        self.config_path = config_path

        if self.config_path is not None and self.type.base_type.config is None:
            raise SemanticError("Config not allowed for instance of type " + self.type.base_type.name + " which has no config")

    def __str__(self):
        return "%s: %s %s" % (
                self.__class__.__name__,
                self.type,
                self.name)

