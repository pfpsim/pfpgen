# -*- coding: utf-8 -*-
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


from .SymbolTable import SymbolTable
from .hlir.Hlir import Hlir
from .hlir import PE, CE, Interface, Service
from .SemanticError import SemanticError
from ..logger import logger as log

import sys

class Analyzer(object):
    def __init__(self):
        self.symbols = SymbolTable()
        # Assume only one instance of this running at once
        SemanticError.n_errors = 0

    def analyze(self, ast):
        if ast is None:
            log.error("No input")
            SemanticError.n_errors += 1
            return

        ast.analyze_pass_1(self.symbols)
        ast.analyze_pass_2(self.symbols)

    def get_n_errors(self):
        return SemanticError.n_errors

    def get_hlir(self, name):

        hlir = Hlir(name)

        try: hlir.top_level_PE = self.symbols['top']
        except SemanticError as e:
            log.error(e.message)
            return None

        if type(hlir.top_level_PE) is not PE:
            log.error(
                    "Top level module must be a PE, not a "
                    + hlir.top_level_PE.__class__.__name__)
            SemanticError.n_errors += 1
            return None

        for item in self.symbols.get_all():
            if item.__class__ is PE:
                hlir.pe_members.append(item)
            elif item.__class__ is CE:
                hlir.ce_members.append(item)
            elif item.__class__ is Interface:
                hlir.interfaces.append(item)
            elif item.__class__ is Service:
                hlir.services.append(item)

        return hlir

    def get_symbols(self):
        return self.symbols

    def debug_print(self):
        self.symbols.debug_print()
