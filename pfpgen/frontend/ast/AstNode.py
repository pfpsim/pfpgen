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


from ..logger import logger as log
from ..semantic import SemanticError

import traceback

class AstNode(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def analyze_pass_1(self, symbol_table):
        try:
            self._analyze_pass_1(symbol_table)
        except SemanticError as e:
            log.error("Line " + str(self.lineno) + " " + e.message + "\n")


    def analyze_pass_2(self, context):
        try:
            self._analyze_pass_2(context)
        except SemanticError as e:
            log.error("Line " + str(self.lineno) + " " + e.message + "\n")
