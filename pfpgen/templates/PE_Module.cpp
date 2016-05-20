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
::
#include "./${Classname}.h"
#include <string>

:: ''' Resolve if the Constructor needs No. of Ports Arguments '''
:: ''' For PEs that have interfaces/ports that are arrays whose size is resolved from bindings'''
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
:: ModuleBaseclass_constructor_ports_literal = ""
:: for items in portslist:
::  constructor_ports_literal = constructor_ports_literal + ", " + "int "+ items + "PortSize"
::  ModuleBaseclass_constructor_ports_literal = ModuleBaseclass_constructor_ports_literal + "," + items + "PortSize"
:: #endfor
:: AdditionalBaseClasses = ""
:: if PE == PETOP:
::  AdditionalBaseClasses = ", DebuggerUtilities() "
:: #endif
::
::
:: if not portslist:
${Classname}::${Classname}(sc_module_name nm, ${Baseclass}* parent,std::string configfile ):${ModuleBaseclass}(nm,parent,configfile) ${AdditionalBaseClasses}{  // NOLINT(whitespace/line_length)
:: else:
${Classname}::${Classname}(sc_module_name nm #{constructor_ports_literal}, ${Baseclass}* parent, std::string configfile):${ModuleBaseclass}(nm ${ModuleBaseclass_constructor_ports_literal},parent,configfile) ${AdditionalBaseClasses}{  // NOLINT(whitespace/line_length)
:: #endif
  /*sc_spawn threads*/
:: if PE == PETOP:
  ThreadHandles.push_back(
    sc_spawn(
      sc_bind(&top::notify_observers, this, this)));
:: #endif
}

void ${Classname}::init() {
:: if PE == PETOP:
  #ifdef PFPSIM_DEBUGGER
    attach_observer(debug_obs);
    if (PFP_DEBUGGER_ENABLED) {
      debug_obs->enableDebugger();
      debug_obs->waitForRunCommand();
    }
  #endif

  #ifndef PFPSIM_DEBUGGER
    if (PFP_DEBUGGER_ENABLED) {
      std::cerr << "\n" << On_IRed
                << "ERROR: Please compile with PFPSIM_DEBUGGER flag for access to"
                << " the debugger. Use: cmake -DPFPSIMDEBUGGER=ON ../src/ in the"
                << " build directory." << txtrst << std::endl;
      return 1;
    }
  #endif
:: #endif
  init_SIM(); /* Calls the init of sub PE's and CE's */
}
void ${Classname}::${PE.name}_PortServiceThread() {
  // Thread function to service input ports.
}
void ${Classname}::${PE.name}Thread(std::size_t thread_id) {
  // Thread function for module functionalty
}
