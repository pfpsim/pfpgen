#!/usr/bin/env python2.7
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


import ply.lex as lex
from .logger import logger as log

from .errors import errorlog

literals = "{}[]():.,;'"
# single quote is there for error detection only

reserved = {
        'interface'        : 'INTERFACE',
        'service'          : 'SERVICE',
        'CE'               : 'COMMUNICATION_ELEMENT',
        'implements'       : 'IMPLEMENTS',
        'PE'               : 'PROCESSING_ELEMENT',
        'bind'             : 'BIND',
        'import'           : 'IMPORT',
        }

tokens = [
        'INT_LITERAL',
        'STR_LITERAL',
        'ID',
        ] + list(reserved.values())

t_ignore  = ' \t'

def t_newline(t):
    r'\r?\n'
    t.lexer.lineno += 1
    return None

def t_INT_LITERAL(t):
    r'(0|[1-9][0-9]*)'
    t.value = int(t.value)
    return t

def t_STR_LITERAL(t):
    r'"(([^"]|\\")*)"'
    t.value = t.lexer.lexmatch.group(5) # for some reason it's group 5
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # Check for reserved words
    t.type = reserved.get(t.value,'ID')
    return t

def t_COMMENT(t):
    r'//.*'
    pass

def t_MCOMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lineno += t.value.count('\n')

def t_error(t):
    t.value = t.value[0]

    errorlog.log_error(t, "Illegal character {token} encountered")

    t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
    lex.runmain()
