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

from . import Interface, CE, Service, PE
from ..SemanticError import SemanticError


class Binding:
    """
    bindings are : interface -> CE implementing interface
                   service   -> PE implementing service

                   interface -> interface if crossing hierarchy
                   service   -> service   if crossing hierarchy
                        binds to local object inside PE

    """
    def __init__(self, src, dst):
        self.source      = src
        self.destination = dst

        srctype = src.get_base_type()
        dsttype = dst.get_base_type()

        if srctype.__class__ is Interface:
            if dsttype.__class__ is CE:
                if srctype not in dsttype.interfaces:
                    # Interface to a CE *NOT* implementing that interface type is an error
                    raise SemanticError("Binding destination " + str(dsttype) + " must implement interface " + str(srctype))
            elif dsttype.__class__ is Interface:
                if srctype is not dsttype:
                    # Interface to a different type of interface is an error
                    raise SemanticError("Cannot bind two interfaces of non-matching types (" + str(srctype) + " and " + str(dsttype) + ")")
                elif src.get_parent().get_base_type().__class__ is not PE:
                    # Interface to interface bindings must be across hierarchy
                    raise SemanticError("Binding from Interface to interface must be across hierarchy")
            else:
                # Interface to something other than an interface or CE is an error
                raise SemanticError("Cannot bind an Interface to a " + dsttype.__class__.__name__)

        elif src.get_base_type().__class__ is Service:
            if dsttype.__class__ is PE:
                if srctype not in dsttype.services:
                    # Service to a PE *NOT* implementing that service is an error
                    raise SemanticError("Binding destination " + str(dsttype) + " must implement service " + str(srctype))
            elif dsttype.__class__ is Service:
                if srctype is not dsttype:
                    # Service to a different type of service is an error
                    raise SemanticError("Cannot bind two services of non-matching types (" + str(srctype) + " and " + str(dsttype) + ")")
                elif src.get_parent().get_base_type().__class__ is not PE:
                    # Interface to interface bindings must be across hierarchy
                    raise SemanticError("Binding from Service to Service must be across hierarchy")
            else:
                # Service to anything but a service or a PE is an error
                raise SemanticError("Cannot bind a Service to a " + dsttype.__class__.__name__)

        else:
            # Binding from anything but an Interface or a Service is an error
            raise SemanticError("Binding source must be a Service or an Interface, not a "    + srctype.__class__.__name__)

    def __str__(self):
        return self.__class__.__name__ + "\n    " + str(self.source) + " ==>> \n    " + str(self.destination)
