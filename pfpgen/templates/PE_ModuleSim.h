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
#ifndef ${Classname}_H_
#define ${Classname}_H_
#include "pfpsim/pfpsim.h"
::
:: ''' Headers for Depedencies '''
:: ''' Interfaces inside PE '''
:: interfacelist =[]
:: for interfaces in PE.interfaces :
::      interfacelist.append(interfaces.type.base_type.name)
:: #endfor
:: interfaceset = set(interfacelist) #make unique and ordered
:: interfacesuniquelist = list(interfaceset) #get a list back
:: for interfaces in interfacesuniquelist :
#include "../behavioural/${interfaces}.h"
:: #endfor
::
:: ''' PE Instances inside this PE '''
:: PEMemberslist =[]
:: for pe_members in PE.pe_members :
::     PEMemberslist.append(pe_members.type.base_type.name)
:: #endfor
:: PEMembersSet = set(PEMemberslist)
:: PEMembersUniqueList = list(PEMembersSet)
:: for pe_members in PEMembersUniqueList :
#include "../behavioural/${pe_members}.h"
:: #endfor
::
:: ''' CE Instances inside this PE '''
:: CEMemberslist =[]
:: for ce_members in PE.ce_members :
::     CEMemberslist.append(ce_members.type.base_type.name)
:: #endfor
:: CEMembersSet = set(CEMemberslist)
:: CEMembersUniqueList = list(CEMembersSet)
:: for ce_members in CEMembersUniqueList :
#include "../behavioural/${ce_members}.h"
:: #endfor
::
:: ''' Services that this PE implements'''
:: Serviceslist =[]
:: for service in PE.services :
::     Serviceslist.append(service.name)
:: #endfor
:: ServicesSet = set(Serviceslist)
:: ServicesUniqueList = list(ServicesSet)
:: for service in ServicesUniqueList :
#include "../behavioural/${service}.h"
:: #endfor
:: ''' Services that this PE uses (binds to) '''
:: ServicesMemberslist =[]
:: for service in PE.service_members :
::     ServicesMemberslist.append(service.type.base_type.name)
:: #endfor
:: ServicesSet = set(ServicesMemberslist)
:: ServiceMembersUniqueList = list(ServicesSet)
:: for service in ServiceMembersUniqueList :
#include "../behavioural/${service}.h"
:: #endfor

class ${Classname}:
:: ''' Services that this PE Implements '''
:: for service in PE.services :
  public ${service.name},
:: #endfor
:: ''' Base class for all modules '''
  public ${Baseclass},
  public sc_module
{
public:
::
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
:: for items in portslist:
::  constructor_ports_literal = constructor_ports_literal + ", " + "int "+ items + "PortSize"
:: #endfor
:: if not portslist:
  /*Constructor*/
  ${Classname}(sc_module_name& nm, ${Baseclass}* parent = 0, std::string configfile = "");
:: else:
  /*Constructor*/
  ${Classname}(sc_module_name& nm #{constructor_ports_literal} , ${Baseclass}* parent = 0, std::string configfile = "");
:: #endif
  /*Destructor*/
  virtual ~${Classname}() = default;
:: if PE.interfaces:
  /*Ports*/
:: #endif
:: for ports in PE.interfaces :
::  if ports.type.is_array is True:
  sc_vector<sc_port<${ports.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>>> ${ports.name};
::  elif ports.type.is_array is False:
  sc_port<${ports.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>> ${ports.name};
::  #endif
:: #endfor
::
:: if PE.service_members:
  /*Services*/
:: #endif
:: for service in PE.service_members:
  sc_port<${service.type.base_type.name}> ${service.name};
:: #endfor
::
:: if PE.pe_members:
  /*PEInstances*/
:: #endif
:: for pe_members in PE.pe_members :
:: 	if pe_members.type.is_array is True:
  std::vector<std::shared_ptr<${pe_members.type.base_type.name}>> ${pe_members.name};
:: 	elif pe_members.type.is_array is False:
  std::shared_ptr<${pe_members.type.base_type.name}> ${pe_members.name};
:: 	#endif
:: #endfor
::
:: if PE.ce_members:
  /*CEInstances*/
:: #endif
:: for ce_members in PE.ce_members :
::  if ce_members.type.is_array is True:
  sc_vector<${ce_members.type.base_type.name}<std::shared_ptr<pfp::core::TrType>>> ${ce_members.name};
::  elif ce_members.type.is_array is False:
  ${ce_members.type.base_type.name}<std::shared_ptr<pfp::core::TrType>> ${ce_members.name};
::  #endif
:: #endfor
protected:
  virtual void init_SIM() final; /* Empty Function - Reserved for future use*/
};
#endif /*${Classname}_H_*/
