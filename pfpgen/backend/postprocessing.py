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

import os
import logging

class PostProcessing:

    def __init__(self,verbose,debug,path="",path_to_static=""):

        self.logger = logging.getLogger('PostProcessing')
        self.logger.addHandler(logging.StreamHandler())
        self.configure_logging(verbose,debug)
        self.copyOverStaticFiles(path,path_to_static)

    def copyOverStaticFiles(self,path,pth_static):
        #Copy over libs from static_src_files
        static_files=pth_static+'/static_src_files/*'
        rsync_result = os.system('rsync -a --ignore-existing '+static_files+' '+path+'/src/')
        if rsync_result != 0:
            self.logger.info("Rsync failed with status {}, using (slower) cp instead"
                    .format(rsync_result))
            os.system('cp -arn '+static_files+'/* '+path+'/src/')

        self.logger.info("Post-Processing Pass ")

    def configure_logging(self,verbose,debug):
        #Set appropritate debug levels
        if verbose and not debug:
            self.logginglevel('INFO')
        elif debug:
            self.logginglevel('DEBUG')
        else:
            self.logginglevel('WARNING')

    def logginglevel(self,LEVEL):
        #print ("Setting Level to : "  +LEVEL)
        self.logger.setLevel(LEVEL)
