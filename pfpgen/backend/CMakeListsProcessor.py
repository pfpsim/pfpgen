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

import logging
import sys
import os
class CMakeListsProcessor:
    def __init__(self,template,outputfile,contextdict,clobber=True):
        self.template = template
        self.logger = logging.getLogger('fadgenerator.cmakelists')
        self.clobber = clobber
        self.process(template,outputfile,contextdict)

    '''Wrapper function to check if file exists'''
    def checkIfFileExists(self,filepath):
        return os.path.isfile(filepath)

    def getlinenumber(self,marker):
        fileh = open(self.template,"r")
        linemarkers = []
        for num,line in enumerate(fileh, 0):
            if marker in line :
                linemarkers.append(num)
        fileh.close()
        return linemarkers

    def process(self,template,outputfile,contextdict):
        self.logger.debug("CMakeLists.txt Pre-Processing")
        #open file and read its contents
        cmakelistsfile = open(template, "r")
        cmakelists = cmakelistsfile.readlines()
        cmakelistsfile.close()

        for key, value in contextdict.items():
            linenumlist = self.getlinenumber(key)
            self.logger.debug("For "+ key + " ")
            #self.logger.debug(linenumlist)
            insertion = ""
            for linenums in linenumlist:
                #clump together all the items in list to insert
                if isinstance(value,list):
                    for item in value:
                        #self.logger.debug(item)
                        insertion = insertion+str(item)+'\n'
                else:
                    sys.exit("Invalid List in DICT")

                cmakelists.pop(linenums) # remove the linemarker at the line.
                #do the actual insertion
                #self.logger.debug(insertion)
                cmakelists.insert(linenums, insertion)

        #Write rendered file
        if not(self.clobber): # by default clobber is True
            if self.checkIfFileExists(outputfile):
                # self.logger.warn("Warning: Cache Turned on "+outputfile+" exists -> not generated")
                pass
            else:
                #Flushtofile
                f = open(outputfile, "w")
                cmakelists = "".join(cmakelists)
                f.write(cmakelists)
                f.close()
        else:
            #Flushtofile
            f = open(outputfile, "w")
            cmakelists = "".join(cmakelists)
            f.write(cmakelists)
            f.close()
        self.logger.debug("CMakeLists.txt Pre-Processor Wrote to: " + str(outputfile))
