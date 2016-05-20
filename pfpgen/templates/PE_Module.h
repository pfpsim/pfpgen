:: #
:: # pfpgen: Code generation tool for creating models in the PFPSim Framework
:: #
:: # Copyright (C) 2016 Concordia Univ., Montreal
:: #     Samar Abdi
:: #     Umair Aftab
:: #     Gordon Bailey
:: #     Faras Dewal
:: #     Shafigh Parsazad
:: #     Eric Tremblay
:: #
:: # Copyright (C) 2016 Ericsson
:: #     Bochra Boughzala
:: #
:: # This program is free software; you can redistribute it and/or
:: # modify it under the terms of the GNU General Public License
:: # as published by the Free Software Foundation; either version 2
:: # of the License, or (at your option) any later version.
:: #
:: # This program is distributed in the hope that it will be useful,
:: # but WITHOUT ANY WARRANTY; without even the implied warranty of
:: # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
:: # GNU General Public License for more details.
:: #
:: # You should have received a copy of the GNU General Public License
:: # along with this program; if not, write to the Free Software
:: # Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
:: # 02110-1301, USA.
:: #
:: import logging
:: ''' Template Defines '''
:: Classname = PE.name
:: ModuleBaseclass = PE.name+"SIM"
:: Baseclass = "pfp::core::PFPObject"
:: log = logging.getLogger('fadgenerator')
:: HEADERFILENAME = Classname.upper()
::
:: ''' Determine Base classes for this module '''
:: publicbaseclasses = [ModuleBaseclass]
:: if PE == PETOP:
::  publicbaseclasses.append('DebuggerUtilities')
:: #endif
::  ''' Convert to literal that can be directly inserted '''
:: baseclasses = ['public '+baseclass for baseclass in publicbaseclasses]
:: lastelement = baseclasses[-1]
:: baseclasses = [baseclass+', ' for baseclass in baseclasses[:-1]]
:: baseclasses.append(lastelement)
:: baseclassesstring = "".join(baseclasses)
::
:: ''' Resolve if the Constructor needs No. of Ports Arguments '''
:: ''' For PEs that have interfaces/ports that are arrays whose size is resolved from bindings '''
:: portslists = []
:: for ports in PE.interfaces :
::  if ports.type.is_array is True:
::      if ports.type.array_size is None:
::          portslists.append(ports.name)
::      #endif
::  #endif
:: #endfor
:: portslist = list(set(portslists))
:: constructor_ports_literal = ""
:: for items in portslist:
::  constructor_ports_literal = constructor_ports_literal + ", " + "int "+ items + "PortSize"
:: #endfor
::
::
#ifndef BEHAVIOURAL_${HEADERFILENAME}_H_
#define BEHAVIOURAL_${HEADERFILENAME}_H_
#include <string>
#include <vector>
#include "../structural/${PE.name}SIM.h"

class ${Classname}: ${baseclassesstring} {  // NOLINT(whitespace/line_length)
 public:
  SC_HAS_PROCESS(${Classname});
:: if not portslist:
  /*Constructor*/
  explicit ${Classname}(sc_module_name nm, ${Baseclass}* parent = 0, std::string configfile = "");  // NOLINT(whitespace/line_length)
:: else:
  /*Constructor*/
  ${Classname}(sc_module_name nm #{constructor_ports_literal} , ${Baseclass}* parent = 0, std::string configfile = "");  // NOLINT(whitespace/line_length)
:: #endif
  /*Destructor*/
  virtual ~${Classname}() = default;

 public:
  void init();

 private:
  void ${PE.name}_PortServiceThread();
  void ${PE.name}Thread(std::size_t thread_id);
  std::vector<sc_process_handle> ThreadHandles;
};

#endif  // BEHAVIOURAL_${HEADERFILENAME}_H_
