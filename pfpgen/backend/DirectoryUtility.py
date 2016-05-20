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
import yaml
import logging

class DirectoryUtility:

    def __init__(self,configfile,outputdir="",debuglevel="CRITICAL"):
        self.logger = logging.getLogger('fadgenerator-DirectoryUtility')
        self.logger.addHandler(logging.StreamHandler())
        self.logginglevel(debuglevel)
        self.outputdir=outputdir

        # stream = file(configfile,'r')
        stream = self.read_input(configfile)
        docs =  yaml.load_all(stream)
        for doc in docs:
            # print doc
            dirstruct =  doc['GeneratedDirectory']
            self.parse_dict(dirstruct)
            self.lookupdict = self.inverse_dict(dirstruct)

    def read_input(self,readfile):
        try:
            with open(readfile) as infile:
                return infile.read()
        except IOError as e:
            self.logger.error(e)
            sys.exit(1)


    def logginglevel(self,LEVEL):
        self.logger.setLevel(LEVEL)


    def parse_dict(self,dirstruct,parentpath=""):
        for key,val in dirstruct.items():
            self.logger.debug(" --" + str(key)+str(val))
            self.make_directory(parentpath+key)
            if isinstance(val,list):
                for items in val:
                    if isinstance(items,dict):
                        self.parse_dict(items,str(key+"/"))

    def inverse_dict(self,dirstruct,parentpath=""):
        lookupdict = {}
        for key,val in dirstruct.items():
            self.logger.debug(" --" + str(key)+str(val))
            if isinstance(val,list):
                for items in val:
                    if isinstance(items,dict):
                        appenddict = self.inverse_dict(items,str(key+"/"))
                        lookupdict.update(appenddict)
                    else:
                        lookupdict[str(items)]=str(parentpath+key)
        return lookupdict

    def checkifDir(self,path):
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
            else:
                return False
        else:
            return False

    ''' Function wrapper that makes a Directory'''
    def make_dir(self,path):
        self.logger.debug("Making Directory: " + path)
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    def make_directory(self,path):
        path = self.outputdir+"/"+path
        if not self.checkifDir(path):
            self.make_dir(path)
        else:
            self.logger.info("it exists: "+path)
