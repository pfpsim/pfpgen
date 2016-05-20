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

from .parser   import Parser
from .semantic import Analyzer

NO_RESULT      = "No result"
SYNTAX_ERROR   = "Syntax Error"
SEMANTIC_ERROR = "Semantic Error"
SUCCESS        = "Success"

class Compiler(object):

    def __init__(self, import_manager):
        self.result = NO_RESULT
        self.import_manager = import_manager
        self.analyzer = Analyzer()

    def compile(self, data):
        parser = Parser(self.import_manager)
        ast = parser.parse(data)

        if parser.get_n_parse_errors() != 0:
            self.result = SYNTAX_ERROR
            return False

        self.analyzer.analyze(ast)

        if self.analyzer.get_n_errors() == 0:
            self.result = SUCCESS
            return True
        else:
            self.result = SEMANTIC_ERROR
            return False

    def compile_to_hlir(self, data, name):
        self.compile(data)

        if self.result == SUCCESS:
            hlir = self.analyzer.get_hlir(name)
            if self.analyzer.get_n_errors() != 0:
                self.result = SEMANTIC_ERROR
            return hlir
        else:
            return None

    def compile_to_symbols(self, data):
        self.compile(data)

        if self.result == SUCCESS:
            return self.analyzer.get_symbols()
        else:
            return None
