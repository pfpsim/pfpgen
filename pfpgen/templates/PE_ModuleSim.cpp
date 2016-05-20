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
:: Classname = PE.name+"SIM"
:: Baseclass = "pfp::core::PFPObject"
:: log = logging.getLogger('fadgenerator')
::
#include "${Classname}.h"
/*PE SIM Constructor*/
:: ''' --Resolve Ports of Array Type-- '''
::
:: portslists = []
:: for ports in PE.interfaces :
::  if ports.type.is_array is True:
::      if ports.type.array_size is None:
::          portslists.append(ports.name)
::      #endif
::  #endif
:: #endfor
:: portslist = list(set(portslists))
:: ''' Construct Literal for Ports if any '''
:: constructor_ports_literal = ""
:: for items in portslist:
::  constructor_ports_literal = constructor_ports_literal + ", " + "int "+ items + "PortSize"
:: #endfor
::
:: if not portslist:
${Classname}::${Classname}(sc_module_name& nm, ${Baseclass}* parent,std::string configfile ):
:: else:
${Classname}::${Classname}(sc_module_name& nm #{constructor_ports_literal}, ${Baseclass}* parent, std::string configfile):
:: #endif
::
:: ''' --- Constructor Initliazation List ---'''
:: ''' Init Ports '''
:: for ports in PE.interfaces :
:: if ports.type.is_array is False:
  ${ports.name}("${PE.name}_${ports.name}"),
:: #endif
:: #endfor
::
:: ''' --- Select sub PE instances  Consturctor based on Binding Lookups --- '''
:: PENameBindingLookup = []
:: for item in PE.bindinglookup:
::  PENameBindingLookup.append(item[0].name)
:: #endfor
::
:: for pe_members in PE.pe_members :
:: 	if pe_members.type.is_array is False:
:: 		if pe_members.config_path==None :
:: 			if not (pe_members.name in PENameBindingLookup):
  ${pe_members.name} (std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}",this)),
:: 			else:
:: 				literal = PE.BindingLiteralLookupDict[pe_members.name] # NOTE: literal already has a leading comma
	${pe_members.name} (std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}"#{literal},this)),
:: 			#endif
:: 		else:
:: 			if not (pe_members.name in PENameBindingLookup):
  ${pe_members.name} (std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}",this,"${pe_members.config_path}")),
:: 			else:
:: 				literal = PE.BindingLiteralLookupDict[pe_members.name] # NOTE: literal already has a leading comma
  ${pe_members.name} (std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}"#{literal},this,"${pe_members.config_path}")),
:: 			#endif
:: 		#endif
:: 	#endif
:: #endfor
:: ''' CE inside the PE '''
:: for ce_members in PE.ce_members :
:: 	if ce_members.type.is_array is False :
::    if ce_members.config_path==None :
  ${ce_members.name} ("${ce_members.name}",this),
::    else:
  ${ce_members.name} ("${ce_members.name}",this,"${ce_members.config_path}"),
::    #endif
:: 	#endif
:: #endfor
::
:: if PE.config is not None:
  ${Baseclass}(pfp::core::convert_to_string(nm), CONFIGROOT+"${PE.config}", CONFIGROOT+configfile, parent),
:: else:
  ${Baseclass}(pfp::core::convert_to_string(nm), parent),
:: #endif
  sc_module(nm)
:: ''' --- Constructor Body --- '''
{
::
:: for pe_members in PE.pe_members :
::  if pe_members.type.is_array is True:
::    if not (pe_members.name in PENameBindingLookup):
::      if pe_members.config_path==None :
  for(int i=0; i<${pe_members.type.array_size};i++){
    std::string pe_name = "${pe_members.name}["+std::to_string(i)+"]";
    ${pe_members.name}.push_back(std::make_shared<${pe_members.type.base_type.name}>(pe_name.c_str(),this));
	}
::      else:
  for(int i=0; i<${pe_members.type.array_size};i++){
    std::string pe_name = "${pe_members.name}["+std::to_string(i)+"]";
    ${pe_members.name}.push_back(std::make_shared<${pe_members.type.base_type.name}>(pe_name.c_str(),this,"${pe_members.config_path}"));
  }
::      #endif
::    else:
::      for index in range(0,pe_members.type.array_size):
:: 				literal = PE.BindingLiteralLookupDict[pe_members.name+"["+str(index)+"]"] # NOTE: literal already has a leading comma
::        if pe_members.config_path == None:
  ${pe_members.name}.push_back(std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}[#{index}]"#{literal},this));
::        else:
  ${pe_members.name}.push_back(std::make_shared<${pe_members.type.base_type.name}>("${pe_members.name}[#{index}]"#{literal},this,"${pe_members.config_path}"));
::       #endif
::      #endfor
::    #endif
::  #endif
:: #endfor
::
:: ''' CE Memebers that arrays '''
:: for ce_members in PE.ce_members :
:: 	if ce_members.type.is_array is True:
::    if ce_members.config_path==None :
  auto make_${ce_members.name} = [&](const char* nm, std::size_t){return new ${ce_members.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>(sc_gen_unique_name("${ce_members.name}"),this); };
  ${ce_members.name}.init(${ce_members.type.array_size},make_${ce_members.name});
::    else:
  auto make_${ce_members.name} = [&](const char* nm, std::size_t){return new ${ce_members.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>(sc_gen_unique_name("${ce_members.name}"),this,"${ce_members.config_path}"); };
  ${ce_members.name}.init(${ce_members.type.array_size},make_${ce_members.name});
::    #endif

:: 	#endif
:: #endfor
::
:: ''' Init the ports which are arrays '''
:: for ports in PE.interfaces:
:: 	if ports.type.is_array is True:
:: 		if not(ports.type.array_size==None):
:: 			size = ports.type.array_size
:: 		elif ports.type.array_size==None:
:: 			size = ports.name + 'PortSize'
:: 		#endif
  ${ports.name}.init(${size}, [](const char* nm, std::size_t) { return new sc_port<${ports.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>>(nm); });
:: 	#endif
:: #endfor
	/* Bindings */
:: for binding in bindings:
  ${binding}
:: #endfor
:: ''' --- Add Children PE's && CE's to this modules children list --- '''
:: for childPE in PE.pe_members:
::	if not(childPE.type.is_array):
  AddChildModule(${childPE.name}->module_name(),${childPE.name}.get());
:: #endif
:: #endfor
:: for childPE in PE.pe_members:
::	if childPE.type.is_array:
  for(int i=0; i<${childPE.type.array_size};i++){
    AddChildModule(${childPE.name}[i]->module_name(),${childPE.name}[i].get());
  }
:: #endif
:: #endfor
}
/* Empty Function - Reserved for future use*/
void ${Classname}::init_SIM(){
	/*Init Sub PE instances*/
:: ''' Call init for all Sub PEs '''
:: for pe_members in PE.pe_members :
:: 	if pe_members.type.is_array is False:
	${pe_members.name}->init();
::	#endif
:: #endfor
::
:: for pe_members in PE.pe_members :
:: 	if pe_members.type.is_array is True:
  for(int i=0; i<${pe_members.type.array_size};i++){
    ${pe_members.name}[i]->init();
  }
::	#endif
:: #endfor
}
::
:: '''=============TODO LOG======================'''
:: ''' --------- Change Log ---------------------'''
:: ''' --Added Logger Object ; LS '''
:: ''' --Changed Init order ; LS '''
:: ''' --Added PE Arrays ; LS'''
:: ''' --Configs are now loaded bt the PFPSIMCore Baseclass ; LS '''
