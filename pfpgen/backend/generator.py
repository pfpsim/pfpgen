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
from operator import itemgetter

import tenjin
from tenjin.helpers import *
import logging
from time import sleep,time

from .CMakeListsProcessor import *
from .DirectoryUtility import *

OutputDirName = "src"
OutputDirUserFiles = "src"
OutputDirSimFiles  = "src/simsrc"

''' Custom Output Defines'''
MAGENTA = '\033[35m'
BOLD_YELLOW = '\033[1;33m'
RESET = '\033[00m'

STREAM = sys.stderr
MILL_TEMPLATE = '\r[\033[1;32m%i\033[00m/%i] %s \033[1;32m%s\033[00m'
CLEAR_WHOLE_LINE = '\x1b[2K'
MILL_CHARS = ['|', '/', '-', '\\']
# How long to wait before recalculating the ETA
ETA_INTERVAL = 1
# How many intervals (excluding the current one) to calculate the simple moving
# average
ETA_SMA_WINDOW = 9
WARNING_TEMPLATE = '\033[1;33m %s - [%s]\033[00m %s'

class fadgen:
    def __init__(self,fadobj):
        self.fadobj = fadobj
        self.Sources = {
            "Structural" : [],
            "Behavioural": []
        }
        self.logger = logging.getLogger('fadgenerator')
        self.logger.addHandler(logging.StreamHandler())
        self.torender = []

    def configure(self,verbose,debug,pathtotemplates,cacheFlag=False,FancyOutput=True):

        self.cache = cacheFlag #Caching
        #Set appropritate debug levels
        if verbose and not debug:
            self.logginglevel('INFO')
        elif debug:
            self.logginglevel('DEBUG')
        else:
            self.logginglevel('WARNING')

        self.templatefilepath = pathtotemplates
        self.init_dir()

        self.FancyOutput = FancyOutput

    def init_dir(self):
        self.make_directory(str(self.fadobj.name))
        dirinfo = DirectoryUtility(self.templatefilepath+"/ConfigureProjectDirectory.yaml",str(self.fadobj.name))
        global OutputDirName
        OutputDirName = str(self.fadobj.name)+"/"+str(dirinfo.lookupdict["Base Source"])
        global OutputDirUserFiles
        OutputDirUserFiles = str(self.fadobj.name)+"/"+str(dirinfo.lookupdict["User Code"])
        global OutputDirSimFiles
        OutputDirSimFiles  = str(self.fadobj.name)+"/"+str(dirinfo.lookupdict["SIM Code"])

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
        if not self.checkifDir(path):
            self.make_dir(path)
        else:
            self.logger.info("it exists: "+path)


    def logginglevel(self,LEVEL):
        #print ("Setting Level to : "  +LEVEL)
        self.logger.setLevel(LEVEL)

    def TempaltingEngine(self,contextdict,templatefile):
        #template preprocessor Arguments Parser
        pp = [
        tenjin.TemplatePreprocessor(),      # same as preprocess=True
        #tenjin.TrimPreprocessor(),          # trim spaces before tags
        tenjin.PrefixedLinePreprocessor(),  # convert ':: ...' into '<?py ... ?>'
        ]
        engine = tenjin.Engine(pp=pp,path=[self.templatefilepath],cache=False,
                # Do not do any HTML escaping or other special magic
                escapefunc="str", tostrfunc="str")
        # render template with context data
        render = engine.render(templatefile,contextdict)
        return render

    def FeedFilePipe(self,contextdict,templatefile,filename):
        self.torender.append([contextdict,templatefile,filename])

    def ExecuteFilePipe(self):
        what = 0
        message = ["Processing "+self.torender[what][2]] # strings are immutable
        starttime = time()
        for i in self.mill(range(len(self.torender)),message,self.FancyOutput):

            #Generate the actual thing
            self.generatefile(self.torender[i][0],self.torender[i][1],self.torender[i][2])

            #Next thing to process
            if (what < len(self.torender)-1):
                what = what + 1
                message[0] = "Processing "+self.torender[what][2]

        done_output = "Done in ... "+str(time()-starttime)
        # TODO(gb) why is logic inverted?
        if not self.FancyOutput:
            STREAM.write(done_output + "\n")
        else:
            print(done_output)

    # Taken from Clint - It can't do what we want ... yet
    # https://github.com/kennethreitz/clint
    # https://pypi.python.org/pypi/clint/
    def mill(self, it, label='',simple_output=False, hide=None, expected_size=None, every=1):
        """Progress iterator. Prints a mill while iterating over the items."""
        def _mill_char(_i):
            if _i >= count:
                return ' '
            else:
                return MILL_CHARS[(_i // every) % len(MILL_CHARS)]

        def _show(_i):
            if not hide:
                if ((_i % every) == 0 or         # True every "every" updates
                    (_i == count)):            # And when we're done

                    if not simple_output:
                        STREAM.write(CLEAR_WHOLE_LINE)
                        STREAM.write(MILL_TEMPLATE % (
                            _i, count, _mill_char(_i), "".join(label)))
                        STREAM.flush()
                    else:
                        print ("["+str(_i)+"/"+str(count)+"] "+"".join(label))

        count = len(it) if expected_size is None else expected_size

        if count:
            _show(0)

        for i, item in enumerate(it):
            yield item
            _show(i + 1)

        if not hide:
            STREAM.write('\n')
            STREAM.flush()

    def WARN(self,message):
        if not self.FancyOutput:
            #STREAM.write('\n')
            #STREAM.flush()
            STREAM.write(CLEAR_WHOLE_LINE)
            STREAM.write('\r'+message+'\n')
            STREAM.flush()
        else:
            self.logger.warn(message)

    def generatefile(self,contextdict,templatefile,filename):
        renderedfile = self.TempaltingEngine(contextdict,templatefile)
        #Determine where to write the file to and check if caching is turned on or not
        if "SIM" in filename: #place *SIM.* files in /src/sim
            filepath = str(OutputDirSimFiles+"/"+filename)
            self.Sources["Structural"].append(filepath)
            if self.checkIfFileExists(filepath):
                if self.checkIfFileisSame(filepath,renderedfile):
                    pass
                else:
                    self.flushtofile(filepath,renderedfile)
                    self.WARN(WARNING_TEMPLATE % ("INFO","Structural", "Out of Date - Updated: "+filepath+" "))

            else:
                self.flushtofile(filepath,renderedfile)
                #self.logger.warn("\033[1;32m[Structure] Generated "+filepath+"\033[00m")

        else:
            filepath = str(OutputDirUserFiles+"/"+filename)
            self.Sources["Behavioural"].append(filepath)
            if(not(self.cache)): # Cache is not turned on write to file regardless
                self.flushtofile(filepath,renderedfile)
                self.WARN(WARNING_TEMPLATE % ("WARNING","Behavioural", "Overwrote existing "+filepath+" ["+MAGENTA+"--nocache"+RESET+"]"))
            else: # Cache is turned on. do not overwrite if file exists
                if self.checkIfFileExists(filepath):
                    pass
                else:
                    self.flushtofile(filepath,renderedfile)
                    #self.logger.warn("[Behaviour] Generated "+filepath)


    '''Wrapper function to check if file exists'''
    def checkIfFileExists(self,filepath):
        return os.path.isfile(filepath)

    def checkIfFileisSame(self,filepath,filecontents):
        file_handle = open(filepath,"r")
        read_contents = file_handle.read()
        file_handle.close()
        if (read_contents == filecontents):
            return True
        else:
            return False

    def flushtofile(self,filepath,filecontents):
        #Write it all to a file
        file_handle = open(filepath,"wb+")
        # file_handle.write(filecontents) #python2
        # file_handle.write(bytes(filecontents, 'UTF-8')) #python3
        file_handle.write(filecontents.encode('UTF-8'))
        file_handle.close()
        self.logger.debug( "Wrote "+filepath )

    def generateinterfaces(self):
        self.logger.debug( 'Generating Interface Header Files' )
        for interface in self.fadobj.interfaces:
            self.logger.debug( "Generating for: "+interface.name )
            self.logger.debug( interface )
            context={}
            context['interface_name']=interface.name
            self.FeedFilePipe(context,'interfacetemplate.h',str(interface.name+".h"))

    def generateservices(self):
        self.logger.debug( 'Generating Service Header Files' )
        for service in self.fadobj.services:
            self.logger.debug( "Generating for: "+service.name )
            self.logger.debug( service )
            context={}
            context['service_name']=service.name
            self.FeedFilePipe(context,'servicetemplate.h',str(service.name+".h"))

    def generateCE(self):
        self.logger.debug( 'Generating CE header Files' )
        for CE in self.fadobj.ce_members:
            self.logger.debug( "Generating for: "+CE.name )
            self.logger.debug( CE )
            context={}
            context['CE']=CE
            self.FeedFilePipe(context,'CEtemplate.h',str(CE.name+".h"))
            self.FeedFilePipe(context,'CE_ModuleSim.h',str(CE.name+"SIM.h"))
            self.FeedFilePipe(context,'CE_ModuleSim.cpp',str(CE.name+"SIM.cpp"))

    def MakeContextDict(self,PE,AttributeName=""):
        attributes = dir(PE) #Get names of all attributes
        #print attributes
        context = {}
        for i,attribute in enumerate(attributes):
            context[AttributeName+attribute] = getattr(PE,attributes[i])
        return context

    def generatePEheader(self,PE):
        self.logger.debug( 'Generating PE header File' )
        self.logger.debug( "Generating for: "+PE.name )
        self.logger.debug( PE )

        def subref_to_string(subref):
            if subref.is_array_reference():
                return "%s[%d]" % (subref.instance.name, subref.index)
            else:
                return subref.instance.name

        binding_statements = []

        for binding in PE.bindings:
            src = '->'.join(map(subref_to_string, binding.source))
            dst = '->'.join(map(subref_to_string, binding.destination))
            # TODO(gordon) .__class__.__name__ is *REALLY* ugly and brittle
            if binding.destination.get_base_type().__class__.__name__ is "PE":
                dst = "*(%s.get())" % dst
            binding_statements.append( "%s.bind(%s);" % (src, dst) )


        context={
            "PE":PE,
            "bindings":binding_statements,
            "PETOP":self.fadobj.top_level_PE
            }


        self.FeedFilePipe(context,'PE_Module.h',str(PE.name+".h"))
        self.FeedFilePipe(context,'PE_Module.cpp',str(PE.name+".cpp"))
        self.FeedFilePipe(context,'PE_ModuleSim.h',str(PE.name+"SIM.h"))
        self.FeedFilePipe(context,'PE_ModuleSim.cpp',str(PE.name+"SIM.cpp"))


    def generatePE(self):
        self.logger.debug( 'Generating PE Files' )
        for PE in self.fadobj.pe_members:
            self.generatePEheader(PE)

    def generateCmakeLists(self):
        self.logger.debug( 'Generating CMakeLists.txt' )
        stripped_structuralsrcs = []
        stripped_behaviouralsrcs = []

        self.Sources["Structural"].append(OutputDirSimFiles+"/"+"pfp_boot.cpp")
        self.Sources["Structural"].append(OutputDirSimFiles+"/"+"create_top.cpp")
        self.Sources["Behavioural"].append(OutputDirUserFiles+"/"+"main.cpp")

        #Sources contains full path from projectname to file, to get file name we strip the whole path
        for obj in self.Sources["Structural"]:
            stripped_structuralsrcs.append("${CMAKE_CURRENT_SOURCE_DIR}"+obj[len(OutputDirSimFiles):])

        for obj in self.Sources["Behavioural"]:
            stripped_behaviouralsrcs.append("${CMAKE_CURRENT_SOURCE_DIR}"+obj[len(OutputDirUserFiles):])

        #Behavioural/CMakelists.txt
        context = {}
        context['<sourcesmarker>'] = stripped_structuralsrcs
        CMakeListsProcessor(str(self.templatefilepath+'/StructuralCMakeLists.txt'),OutputDirSimFiles+'/CMakeLists.txt',context)
        #Structural/CMakelists.txt
        context = {}
        context['<sourcesmarker>'] = stripped_behaviouralsrcs
        CMakeListsProcessor(str(self.templatefilepath+'/BehaviouralCMakeLists.txt'),OutputDirUserFiles+'/GeneratedSources.cmake',context)
        #MasterCMakeLists.txt
        context = {}
        context['<ProjectName_marker>'] = [str(self.fadobj.name)]
        context['<Executable_marker>']  = [str(self.fadobj.name)+"-sim"]
        CMakeListsProcessor(str(self.templatefilepath+'/MasterCMakeListsTemplate.txt'),OutputDirName+'/CMakeLists.txt',context,False)


    '''
    TODO: REWIRTE THIS MODULE - BindingResolutionPass
    '''
    def BindingResolutionPass(self):
        #self.fadobj <---- Is the minified Fad Representation
        PeList = [] # This list will have PE's for which whose interfaces are of array type and whose size is undefined
        for PE in self.fadobj.pe_members:
            self.logger.debug("For: " + PE.name + " Has Interfaces:")
            for interface in PE.interfaces:
                self.logger.debug(" |-" + interface.name)
                self.logger.debug("     |- Array:" + str(interface.type.is_array))
                if interface.type.is_array is True :
                    self.logger.debug("      |-Size: " + str(interface.type.array_size))
                    if interface.type.array_size is None:
                        PeList.append([PE,interface.name])

        #self.fadobj.
        self.logger.debug("PE's Found:")
        for items in PeList:
            self.logger.debug(items)

        self.logger.debug('\n'+'-----PE Instances-------'+'\n')
        # Make sure that they all have this attribute
        for pe in self.fadobj.pe_members:
            if not hasattr(pe,'bindinglookup'):
                pe.bindinglookup = []

        #Now to find the instances and resolve binding counts for those instances of these PE's
        for PEtoLookup in PeList:
            self.logger.debug("-----------------------------")
            for i, PE in enumerate(self.fadobj.pe_members):
                for j, PEInstance in enumerate(PE.pe_members):
                    if PEInstance.type.base_type.name == PEtoLookup[0].name:
                        # Now do a binding count
                        if PEInstance.type.is_array is False:
                            interfacecount = 0
                            for binding in PE.bindings:
                                ''' Name of Instance && Name of Interface of that Instance '''
                                if binding.source[0].instance.name == PEInstance.name and binding.source[1].instance.name == PEtoLookup[1]:
                                    interfacecount=interfacecount+1
                            self.logger.debug("  |- Count:" + str(interfacecount))
                            self.fadobj.pe_members[i].bindinglookup.append([PEInstance,PEtoLookup[1],interfacecount])
                        elif PEInstance.type.is_array is True:
                            for pelookupindex in range(0,PEInstance.type.array_size):
                                interfacecount = 0
                                for binding in PE.bindings:
                                    ''' Name of Instance + index && Name of Interface of that Instance '''
                                    if binding.source[0].instance.name == PEInstance.name and binding.source[0].index == pelookupindex and binding.source[1].instance.name == PEtoLookup[1] :
                                        interfacecount=interfacecount+1
                                #self.logger.debug("  |- Count:" + str(interfacecount))
                                #PE, Interface, Count, PEIndex
                                self.fadobj.pe_members[i].bindinglookup.append([PEInstance,PEtoLookup[1],interfacecount,pelookupindex])


        self.logger.debug('\n'+'-----PE binding lookups-------'+'\n')
        for i, PE in enumerate(self.fadobj.pe_members):
            uniquePElist = []
            PEBindingLookupList = {} #<--- Dict that returns a Compounded Lookup List of Interfaces Binding Count for that PE Instance
            for lookups in PE.bindinglookup:
                #print lookups
                if lookups[0].type.is_array is False:
                    uniquePElist.append(lookups[0].name)
                elif lookups[0].type.is_array is True:
                    uniquePElist.append(lookups[0].name+"["+str(lookups[3])+"]")
            #Make List unique
            uniquePElist=list(set(uniquePElist))

            #for items in uniquePElist:
            #   print(items)

            def name_resolver(obj):
                if obj[0].type.is_array is True:
                    return obj[0].name+"["+str(lookups[3])+"]"
                elif obj[0].type.is_array is False:
                    return obj[0].name

            ''' Now Link the Unique List with the Interface Binding Information '''
            for instance in uniquePElist:
                bindinfo = []
                for lookups in PE.bindinglookup:
                    if name_resolver(lookups) == instance:
                        if lookups[0].type.is_array is False:
                            bindinfo.append([lookups[1],lookups[2]])
                        elif lookups[0].type.is_array is True:
                            bindinfo.append([lookups[1],lookups[2],lookups[3]])
                PEBindingLookupList[instance] = bindinfo

            #for key , val in PEBindingLookupList.items():
            #    print("For Key:" + str(key) + " -> " + str(val))

            ''' prep a lookup dict that the template can directly use to insert the required literal. '''
            BindingLiteralLookupDict = {}
            ''' Prepare Literal that can be directly inserted in the template '''
            for instancename , bindcount in PEBindingLookupList.items():
                ''' Sort the bindcount List according to port/interface name'''
                #print("Sorting For: " + str(instancename))
                #print("Original Binding: " + str(bindcount))
                sortedlist = sorted(bindcount, key=itemgetter(0))
                #print("Sorted Binding" + str(sortedlist))
                ''' Construct the Literal '''
                sortedlist.reverse()
                literal = ''
                for items in sortedlist:
                    literal = literal + ',' + str(items[1])
                #print("Constructed literal is: "+literal)
                BindingLiteralLookupDict[instancename] = literal

            ''' Key: PE Name | Value: Literal '''
            self.fadobj.pe_members[i].BindingLiteralLookupDict = BindingLiteralLookupDict #Assign the LookupDict to the PE object

            '''
            Note on Why ?
            Can't assign the array size to the original interface inside that PE because
            the array size of the interface used in the bindings can be different for
            each Instance of that PE
            '''
    def FindTopLevelPE(self):
        for pe in self.fadobj.pe_members:
            #print pe.name
            if pe.name == "top":
                self.fadobj.top_level_PE = pe

    def GenerationPass(self):
        self.logger.debug( '\nStarting SystemC Code Generation for:  '+self.fadobj.name+'\n' )
        self.FindTopLevelPE()
        # Parallelize all below
        self.generateinterfaces()
        self.generateservices()
        self.generateCE()
        self.generatePE()
        self.ExecuteFilePipe()
        self.generateCmakeLists()
        # End Parallelize
        self.logger.debug( '\nGenerator Done!\n' )

        self.logger.debug( '\n\n-------------------\n\n' )

    def rungenerator(self):
        self.logger.info("HLIR Semantic Check -- \033[1;32mPassed\033[1;m")
        self.logger.info("Generation Pass 1")
        self.BindingResolutionPass()
        self.logger.info("Generation Pass 2")
        self.GenerationPass()
