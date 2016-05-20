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


from .logger import logger

from ply.lex  import LexToken
from ply.yacc import YaccSymbol


class ErrorInstance(object):
    def __init__(self, pos, token, message):
        self.pos     = pos
        self.token   = token
        self.message = message


class ErrorLogger(object):
    def __init__(self):
        self.errors = []

    def reset(self):
        self.errors = []

    def get_n_errors(self):
        return len(self.errors)

    def log_error(self, p, message):
        pos = p.lexpos

        # TODO token not passed properly, but do we even need it?
        self.errors.append(ErrorInstance(pos, p, message.format(token=p.value)))

    def report_errors(self, text):

        def format_line(rawline, index):
            # Get a line which is all spaces and tabs to push our caret
            indicator = ''.join('\t' if c=='\t' else ' ' for c in rawline[:index])
            indicator += '^'

            length = len(rawline)

            if length > 70:
                endpos    = min(length, index + 35)
                startpos  = max(0, endpos - 70)
                rawline   = rawline   [startpos:endpos]
                indicator = indicator [startpos:endpos]

                if startpos != 0:
                    rawline   = '...' + rawline
                    indicator = '   ' + indicator

                if endpos != length:
                    rawline += '...'


            return rawline, indicator

        pos    = 0
        lineno = 1
        err    = 0
        end    = 0
        while err < len(self.errors) and end != -1:
            end = text.find('\n', pos)
            while err < len(self.errors) and pos <= self.errors[err].pos <= end:
                line, indicator = format_line(text[pos:end], self.errors[err].pos - pos)

                logger.error(
                    "Line {lineno}: {msg}\n{line}\n{indicator}\n"
                    .format(lineno=lineno, msg=self.errors[err].message,
                        line=line, indicator=indicator))
                err += 1
            pos = end + 1
            lineno += 1

errorlog = ErrorLogger()
