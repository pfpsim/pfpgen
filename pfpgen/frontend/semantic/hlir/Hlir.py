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

class Hlir:
    def __init__(self,name):
        self.name = name
        self.interfaces = []
        self.services   = []
        self.ce_members = []
        self.pe_members = []
        self.top_level_PE = None
        self.bindings = []
        #self.bind       = [ Bind( Bindobject("src"),[Bindobject("a"),Bindobject("b")] ) ]

    def debug_print(self):
        s = "PE "

        s += self.name
        s += "\n"
        s += " implements " + ', '.join(map(str, self.services))
        s += "\n"

        for interface in self.interfaces:
            s +=" implements"+"  " + str(interface) + "\n"

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

        print (s)
