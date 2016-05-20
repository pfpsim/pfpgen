#!/usr/bin/env python
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


"""pfpgen.pfpgen provides entry point main()."""

from .version import __version__

import argparse
from sys import exit
import logging
import re
import os
from pkg_resources import *

from .frontend.compiler import Compiler, SUCCESS
from .frontend.imports import ImportManager

from .backend.generator import *
from .backend.postprocessing import *

def get_args():
    parser = argparse.ArgumentParser(description='FAD Compiler.')
    parser.add_argument('input', type=str,
                    help='The FAD file to compile')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    parser.add_argument("--verbose", help="increase output verbosity",
                    action="store_true")
    parser.add_argument("--debug", help="increase output verbosity to debug",
	                action="store_true")
    parser.add_argument("--nocache", help="Turns of caching of files",
	                action="store_true")
    parser.add_argument("--nofancyoutput", help="Simple good old fashioned output on stdout ",
	                action="store_true")
    # TODO user include and system include paths
    return parser.parse_args()

def read_input(args):
    try:
        with open(args.input) as infile:
            return infile.read()
    except IOError as e:
        sys.stderr.write("error: file '%s' not found" % args.input)
        sys.exit(1)

def main():
    if resource_exists(__name__,'templates') and resource_isdir(__name__,'templates'):
        template_resource = resource_filename(__name__, 'templates')
    else:
        raise ValueError('PFPGen Code Templates not found - exiting - Please check your installation')
        exit(-1)

    args = get_args()

    filext =  os.path.splitext(args.input)
    if not ('.fad' in str(filext[1]) ):
        raise SystemExit("File should be a .fad")
    filename = os.path.basename(filext[0])

    file_contents = read_input(args)

    compiler = Compiler(ImportManager(["./"],["./"]))

    hlir = compiler.compile_to_hlir(file_contents, filename) # todo make this an arg

    if compiler.result != SUCCESS:
        exit(2)

    genobj = fadgen(hlir)
    #Verbose flag, Debug Flag, Path to templates, cacheFlag is optional default cache is on
    genobj.configure(args.verbose,args.debug,template_resource,not(args.nocache),args.nofancyoutput)
    genobj.rungenerator()

    PostProcessing(args.verbose,args.debug,hlir.name,template_resource)

    if args.verbose:
        print("Done for \033[1;33m"+str(args.input)+"\033[1;m"+" ---> \033[1;34msrc/\033[1;m")
