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


import os,sys
import ply.yacc as yacc
from ply.lex import LexToken
from .tokenizer import tokens

from .logger import logger as log
from .errors import errorlog


from .ast import *

class Parser(object):
    def __init__(self, import_manager):
        self.start = 'program'
        self.tokens = tokens
        errorlog.reset()
        self.import_manager = import_manager
        directory = os.path.expanduser('~/.pfpgen')
        if not os.path.exists(directory):
            os.makedirs(directory)
        sys.path.append(directory)
        self.yacc = yacc.yacc(debug=False, module=self, outputdir=directory)

    def parse(self, indata):
        value = self.yacc.parse(indata, tracking=True)
        errorlog.report_errors(indata)
        return value

    def get_n_parse_errors(self):
        return errorlog.get_n_errors()


    def p_fad_program(self, p):
        '''program : declaration_list '''
        p[0] = Program(p[1])

    def p_empty(self, p):
        '''empty : '''
        pass

    def p_declaration_list(self, p):
        ''' declaration_list : declaration_list declaration
                             | empty'''
        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[2])
            p[0] = p[1]

    def p_declaration(self, p):
        '''declaration : interface_declaration
                       | service_declaration
                       | communication_element_declaration
                       | processing_element_declaration
                       | import_statement '''
        p[0] = p[1]

    def p_import_statement(self, p):
        ''' import_statement : IMPORT dotted_id_list semicolon '''

        p[0] = ImportStatement(p[2], self.import_manager, p.lineno(1))

    def p_dotted_id_list(self, p):
        ''' dotted_id_list : dotted_id_list '.' ID
                           | ID '''

        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]


    def p_semicolon(self, p):
        ''' semicolon : ';' '''

    def p_interface_declaration(self, p):
        '''interface_declaration : INTERFACE plain_member_spec_list semicolon '''
        p[0] = InterfaceDeclaration(p[2], p.lineno(1))

    def p_service_declaration(self, p):
        ''' service_declaration : SERVICE plain_member_spec_list semicolon '''
        p[0] = ServiceDeclaration(p[2], p.lineno(1))

    def p_communication_element_declaration(self, p):
        '''communication_element_declaration : COMMUNICATION_ELEMENT plain_member_spec IMPLEMENTS id_list semicolon '''
        p[0] = CommunicationElementDeclaration(p[2], p[4], p.lineno(1))

    def p_processing_element_declaration(self, p):
        ''' processing_element_declaration : pe_header pe_body semicolon '''

        p[0] = p[1]
        p[0].set_statements(p[2])

    def p_pe_header(self, p):
        ''' pe_header : PROCESSING_ELEMENT plain_member_spec
                      | PROCESSING_ELEMENT plain_member_spec IMPLEMENTS id_list '''
        if len(p) == 3:
            p[0] = ProcessingElementDeclaration(p[2], p.lineno(1))
        else:
            p[0] = ProcessingElementDeclaration(p[2], p.lineno(1), p[4])


    def p_pe_body(self, p):
        ''' pe_body : '{' pe_statements '}' '''
        p[0] = p[2]

    def p_pe_statements(self, p):
        ''' pe_statements : pe_statements member_statement
                          | pe_statements bind_statement
                          | empty '''

        if len(p) == 2:
            p[0] = []
        else:
            p[1].append(p[2])
            p[0] = p[1]

    def p_bind_statement(self, p):
        ''' bind_statement : BIND instance_spec '{' instance_list '}' semicolon '''

        p[0] = BindStatement(p[2], p[4], p.lineno(1))

    def p_instance_list(self, p):
        ''' instance_list : instance_list ',' instance_spec
                          | instance_spec '''
        if len(p) == 2:
            p[0] = [ p[1] ]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_instance_spec(self, p):
        ''' instance_spec : instance_spec '.' instance_fragment
                          | instance_fragment '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_instance_fragment(self, p):
        ''' instance_fragment : ID '[' INT_LITERAL ']'
                              | ID '''
        if len(p) == 2:
            p[0] = InstanceSpecifier(p[1], p.lineno(1))
        else:
            p[0] = InstanceSpecifier(p[1], p.lineno(1), p[3])

    def p_member_statement(self, p):
        ''' member_statement : ID member_list semicolon '''

        p[0] = MemberStatement(p[1], p[2], p.lineno(1))

    def p_member_list(self, p):
        ''' member_list : member_list ',' member_spec
                          | member_spec '''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_member_spec(self, p):
        ''' member_spec : plain_member_spec array_fragment
                        | plain_member_spec '''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[1].set_array_size(p[2])
            p[0] = p[1]

    def p_array_fragment(self, p):
        ''' array_fragment : '[' INT_LITERAL ']'
                           | '[' ']' '''
        if len(p) == 3:
            p[0] = None
        else:
            p[0] = p[2]

    def p_plain_member_spec(self, p):
        ''' plain_member_spec : ID '(' STR_LITERAL ')'
                              | ID '''
        if len(p) == 2:
            p[0] = MemberInstance(p[1], p.lineno(1))
        else:
            p[0] = MemberInstance(p[1], p.lineno(1), p[3])


    def p_plain_member_spec_list(self, p):
        ''' plain_member_spec_list : plain_member_spec_list ',' plain_member_spec
                                   | plain_member_spec '''
        if len(p) == 4:
            p[0] = p[1] + [ p[3] ]
        else:
            p[0] = [ p[1] ]

    def p_id_list(self, p):
        ''' id_list : id_list ',' ID
                    | ID '''
        if len(p) == 4:
            p[0] = p[1] + [ p[3] ]
        else:
            p[0] = [ p[1] ]

    def p_error(self, p):
        if p is None:
            errorlog.log_error(self.yacc.symstack[-1], "Unexpected end of input")
        elif p.value == ';':
            errorlog.log_error(p, "Unexpected semicolon")
        else:
            errorlog.log_error(p, "Unexpected token {token}")
            while p is not None and  p.value != ';':
                p = self.yacc.token()
        self.yacc.restart()

if __name__ == '__main__':

    from sys import argv

    if len(argv) == 2:
        with open(argv[1]) as infile:
            parse(infile.read())
    else:
        print ("No infile")
