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
:: Classname = interface_name
:: log = logging.getLogger('fadgenerator')
:: HEADERFILENAME = Classname.upper()
::
#ifndef BEHAVIOURAL_${HEADERFILENAME}_H_
#define BEHAVIOURAL_${HEADERFILENAME}_H_

#include "systemc.h"  // NOLINT
#include "tlm.h"  // NOLINT
using tlm::tlm_tag;

template <typename T>
class ${interface_name} : public sc_interface {
 public:
    /* User Logic - Virtual Functions for interface go here */
};
#endif  // BEHAVIOURAL_${HEADERFILENAME}_H_
