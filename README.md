# pfpgen [![Build Status](https://travis-ci.org/pfpsim/pfpgen.svg?branch=master)](https://travis-ci.org/pfpsim/pfpgen)

`pfpgen` is the official compiler for the Forwarding Architecture Description Language (FAD).
It makes up the code-generation portion of the PFPSim Framework.

PFPSim is a host-compiled simulation framework for early validation and analysis of packet processing applications on
programmable forwarding plane architectures. Simulation models are automatically generated from a high-level description of
the hardware/software architecture of the forwarding device, written in FAD, and the behavioural description of the
various modules in the architecture, written in C++/SystemC. Our FAD language is capable of defining
[many-core network processors](https://github.com/pfpsim/simple-npu) as well as
[reconfigurable pipelines](https://github.com/pfpsim/simple-rmt).

Application developers can use PFPSim as a virtual prototype to simulate and debug their applications before hardware
availability. Hardware architects can use PFPSim to evaluate the trade-offs between different hardware/software design
decisions.

### Contents
- [**PFPSim Methodology & Workflow**](#pfpsim-methodology--workflow)
  - [Overview](#overview)
  - [Basic Workflow](#basic-workflow)
  - [P4 Workflow](#p4-workflow)
- [**Forwarding Architecture Description Language (FAD)**](#forwarding-architecture-description-language)
  - [Overview](#overview-1)
  - [Basic Language Constructs](#basic-language-constructs)
    - [Processing Elements (PEs)](#processing-elements-pes)
    - [Interfaces](#interfaces)
    - [Communication Elements (CEs)](#communication-elements-ces)
    - [Services](#services)
  - [Example](#example)
  - [Formal Language Specification](#formal-language-specification)
- [**FAD Compiler (`pfpgen`)**](#fad-compiler-pfpgen)
  - [Output](#output)
  - [Arguments](#arguments)
- [**Installation**](#installation)
  - [Using the PFPSim GUI Installer](#using-the-pfpsim-gui-installer)
  - [Manually](#manually)
    - [Prerequisites](#prerequisites)
    - [Dependencies](#dependencies)
    - [Installing](#installing)
      - [Using `pip`](#using-pip)
      - [Using `easy_install`](#using-easy_install)
      - [From source](#from-source)
- [**Developing**](#developing)
  - [Set up](#set-up)
  - [Contributing](#contributing)
- [**Support**](#support)
- [**License**](#license)
- [**Authors**](#authors)

# PFPSim Methodology & Workflow

## Overview

Software-Defined Networking (SDN) enables centralized network control by physical separating the control plane from the forwarding plane. The next logical step in SDN is the ability to fully program the forwarding behavior from the controller, i.e. a Programmable Forwarding Plane. The emergence of new forwarding plane programming languages such as P4 and POF, and highly programmable forwarding hardware such as NPUs and reconfigurable pipelines, is evidence of this growing trend. 

![methodology](https://raw.githubusercontent.com/pfpsim/pfpsim.github.io/master/images/banner-image.png)

PFPSim enables pre-silicon co-design and co-optimization of programmable forwarding plane architecture and applications as seen in the figure above. The forwarding plane designer specifies a mapping between the application (written in P4, C or C++) and the forwarding architecture (described in a simple architecture description language). A model generator (pfpgen) auto-generates a host-compiled simulation binary from the forwarding plane specification. A powerful debugger (pfpdb) enables the designer to debug their application running on a model of the target architecture. The user can also program observers to generate interesting simulation metrics such as packet latency, memory footprint, power consumption etc. to guide pre-silicon optimization of both the application and the forwarding architecture.

## Basic Workflow

The PFPSim workflow aims to provide a clean separation between the structural and behavioural architecture specifications,
the application, and run-time configuration.

![workflow](https://cloud.githubusercontent.com/assets/943241/15302678/36770edc-1b82-11e6-8ddf-3a75ceba7bf9.PNG)

The steps to create and run a PFPSim model are as follows

1. Specify the structure of the target in FAD. FAD descriptions consist of a hierarchy of basic modules, and the
   interconnections between them. The FAD language is described in detail in
   [the next section](#forwarding-architecture-description-language).

   The FAD specification is processed by `pfpgen`, and a SystemC/C++ project corresponding to the specified structure
   is created.

2. While the newly generated project contains a complete implementation of the target's structure, the behaviour is
   still unspecified. The behaviour of the target is written in C++ in the same way it would
   be done in a traditional SystemC project. The key difference is that the repetitive and error prone process of
   creating and modifying modules and their interconnections is managed automatically.

3. Once the target is fully specified, the application can be written. This can be done in C or C++, but may
   also be done in a DSL such as P4, as described below.

4. Next the structure, behaviour and application are compiled with a standard C++ compiler, linking to
   both SystemC and [the PFPSim library](https://github.com/pfpsim/PFPSim), to create the simulation model.

5. The simulation model also optionally accepts run-time configuration (if specified in the FAD model). This
   feature allows for different permutations of design parameters, ranging from memory sizes to scheduling policies,
   to be explored efficiently and conveniently, without requiring constant recompilation of the model.

6. Finally the model can be executed, generating detailed metrics as specified by the designer. These metrics can
   in turn be used to inform the design of the application and target architecture in a rapid cycle of design-space
   exploration and optimization.

## P4 Workflow

We can easily extend the basic workflow outlined above to integrate a DSL such as P4 to describe the application,
further streamlining the design process.

![p4-workflow](https://cloud.githubusercontent.com/assets/943241/15303861/0a2b6a34-1b88-11e6-8e65-37a079c0adc9.PNG)

In this workflow we embed a [P4 runtime environment](https://github.com/p4lang/behavioral-model) into our model.
We use the [P4 compiler](https://github.com/p4lang/p4c-bm) to generate a JSON description of a P4 program,
which becomes an additional piece of runtime configuration to our model.

This further enhances the efficiency of the design and optimization cycle, making it possible to test various architectural
parameters against multiple applications very quickly.

# Forwarding Architecture Description Language
## Overview
The Forwarding Architecture Description Language (FAD)
allows designers to create an abstract specification of the hierarchical structural
model of forwarding devices. FAD provides a few simple
declarative constructs to succinctly specify the hardware-software
platform. This description is used by `pfpgen` to control the generation of
SystemC code.

A detailed description and tutorial of the FAD language is available
[on our wiki](https://github.com/pfpsim/pfpgen/wiki/Forwarding-Architecture-Description-Language-(FAD)).

## Basic Language Constructs
### Processing Elements (PEs)
The `PE` keyword defines a processing element type. It can represent either a
hardware module, such as a parser or CPU core, or a software module, such as
an application or driver.

### Interfaces
The `interface` keyword is used to define a hardware port type which is used for the
connections between hardware modules. Interface types are purely abstract, with all details
other than the name of the interface being left to the behavioural description.

### Communication Elements (CEs)
The `CE` keyword is used to define communication element types, such as passive
memories or links between modules. CEs are very simple elements, a CE instances simply process
transactions initiated by PEs.

CEs and interfaces are closely related. While interfaces provide purely abstract port types,
CEs are the concrete modules providing those port types. In FAD this is represented using the `implements`
keyword, which specifies the interface or interfaces that a given CE provides.

### Services
The `service` keyword is used to define a software service type which is used for the
connections between software modules. Services are very similar to interfaces, the key difference being
that services are implemented by PEs, and that they represent software connections rather than
hardware connections. Conceptually, any PE implementing a service should be thought of as representing
a software layer.

## Example

The following is a simple FAD example that demonstrates all of the language features described above, as well as some
more advanced features. It describes a simple CPU core (`core`) connected to a Memory (`mem`). The CPU core hosts a
hardware abstraction layer (`hal`), and an application (`app`) which communicates with the memory using the HAL.
The whole model is contained within the `top` PE, which has a special role in FAD analogous to `main` in C or C++.

A detailed step-by step tutorial building this example is available
[on our wiki](https://github.com/pfpsim/pfpgen/wiki/Forwarding-Architecture-Description-Language-%28FAD%29#basic-language-constructs-by-example).

```java
interface MemoryIf;

CE Memory implements MemoryIf;

service HALService;

PE HAL implements HALService {
  MemoryIf memory_if;
};

PE Application {
  HALService hal_port;
};

PE Core {
  Application app;
  HAL hal;
  MemoryIf memory_if;

  bind app.hal_port  {hal};
  bind hal.memory_if {memory_if};
};

PE top {
  Core core;
  Memory mem;

  bind core.memory_if {mem};
};
```

Representing this FAD model graphically, it would look like this:

![fad-core-memoryif-memory-bound-hal-app](https://cloud.githubusercontent.com/assets/943241/15339976/1c751a28-1c55-11e6-816f-140e88ed1a24.PNG)

## Formal Language Specification

The formal specification of the grammar and semantics can be found as a work-in-progress on [our wiki](https://github.com/pfpsim/pfpgen/wiki/Formal-Language-Specification).

# FAD Compiler (`pfpgen`)
The official FAD compiler is `pfpgen`. It compiles FAD models into executable SystemC/C++ code, linking against
the [PFPSim library](https://github.com/pfpsim/PFPSim).

The simplest usage of `pfpgen` is simply:

```sh
pfpgen <model.fad>
```

## Output
Running `pfpgen` on a FAD file produces a new CMake based SystemC/C++ project. The project will be created in
a folder that has the same name as the FAD file, with the `.fad` extension removed. For example if we had a FAD file
named `model.fad` and ran `pfpgen model.fad`, the output would be a folder named `model`.

The generated folder has the following layout:

```
model                 - The root
│
├── build             - Initially empty, you should build and run your model here
│   │
│   └── Configs       - Default search path for configuration files.
│
└── src               - Where the code lives
    │
    ├── behavioural   - The C++ code that makes up the behavioural description. This is populated
    │                   with skeletal classes which serve as a starting point for implementing the
    │                   behaviour of the model.
    │
    └── structural    - The C++ code that implements the structure of the model is generated here.
                        This code should not be modified, and we recommend that you don't include
                        it in your version control, but rather treat it essentially as a black box.
```

Subsequent runs of `pfpgen` on the same file from the same directory should have minimal impact on the SystemC/C++
project. Before writing any file in `src/structural`, `pfpgen` will first generate the content for that file in memory.
If a file with the same name already exists on disk, `pfpgen` will only overwrite it if it is different than
the version of the file generated in memory. This prevents causing needless re-compilation of C++ sources that have
not actually been changed, making it fast to make structural changes and recompile the model.

Additionally, `pfpgen` will never overwrite an existing file in `src/behavioural`. Unlike the structural sources, `pfpgen`
considers versions of these files to be "more correct" than the versions it generates if the two are different. This may
occasionally cause minor problems when modifying the FAD file and re-compiling, but generally these can be easily solved
by backing up the original behavioural sources, and using a diff tool to merge the changes.

## Arguments
Generally the default behaviour of `pfpgen` should be all that is needed, however there are some additional
command line arguments which may sometimes be necessary.

- **`--nocache`** This argument forces `pfpgen` to write all behavioural sources whether a file with the same
  name already exists or not.
- **`--nofancyoutput`** This argument disables the "fancy" default output of `pfpgen` and causes it to give a
  plain text output instead.
- **`--verbose`** and **`--debug`** These arguments are meant for `pfpgen` developers, and cause internal logs
  to be output, for use in debugging the compiler itself.


# Installation

## Using the PFPSim GUI Installer
We provide [a text-based GUI installer](https://github.com/pfpsim/pfpsim-installer)
for the PFPSim library, compiler, debugger, and required dependencies. This is
the recommended method for installing this library.

## Manually

### Prerequisites
To install `pfpgen`, you must have:

- Any of the officially supported Python versions (2.7, 3.2, 3.3, 3.4, 3.5)
- Either [`pip`](https://pypi.python.org/pypi/pip) or [`setuptools`](https://pypi.python.org/pypi/setuptools).


### Dependencies
Dependencies are installed automatically, but for the curious, they are the following

- [**PLY (Python Lex-Yacc)**](http://www.dabeaz.com/ply/), which is used for the compiler frontend
- [**Tenjin**](https://pypi.python.org/pypi/Tenjin/), which is used for code-generation
- [**PyYAML**](https://pypi.python.org/pypi/PyYAML), which is used to read internal configuration files for code-generation

If you have `pip` but for some reason want to install these dependencies separately, you can do so:

```sh
pip install ply tenjin pyyaml
```

### Installing
#### Using `pip`

Download the latest wheel (`.whl` file) from [our releases page](https://github.com/pfpsim/pfpgen/releases), and simply run:

```sh
$ pip install pfpgen-X.X.X-py*.whl
```

#### Using `easy_install`
If you absolutely must, you can download the latest `.tar.gz` from
[our releases page](https://github.com/pfpsim/pfpgen/releases) and run:

```sh
$ easy_install pfpgen-X.X.X-pyX.X.tar.gz
```

But [you should use `pip`](http://stackoverflow.com/a/30408520/1084754),
shoot us an email as to why you are still using `easy_install` :wink:.

#### From source
Get a copy of the source, probably by cloning this repository or downloading a source archive from
[our releases page](https://github.com/pfpsim/pfpgen/releases), extract it, and run:

```
$ python setup.py install
```

Most likely this will need to be run under `sudo` in Mac/Linux or with administrator privileges under Windows.

# Developing

## Set up
To work on the `pfpgen` codebase, the first step is obviously to clone this repository. A high level overview
of the structure of the code is as follows.

```
pfpgen
├── dist                     - Currently release binaries are stored here. This will soon be removed
│
└── pfpgen                   - The root of the pfpgen python module, all code lives in subdirectories
    │
    ├── frontend             - The compiler frontend. This includes syntactic analysis, AST construction,
    │   ├── ast                semantic analysis, and High-Level Intermediate Representation (HLIR)
    │   └── semantic           generation, for use by the compiler backend.
    │       └── hlir
    ├── backend              - The compiler backend. This module consumes the HLIR generated by the
    │                          frontend and populates the C++ templates.
    │
    ├── templates            - These are the C++ templates used for code generation. They contain both
    │   │                      C++ and Python code, and are populated using the Python Tenjin library.
    │   │
    │   └── static_src_files - These are C++ files which are copied without modification to the generated
    │       ├── behavioural    C++/SystemC project.
    │       └── structural
    └── tests                - Unit tests and integration tests.
```

In order to try out any changes you make, we recommend that you run:

```
$ python setup.py develop
```

This installs `pfpgen` in your system path so that it can be invoked from anywhere, but links it back to
your development directory so that you do not need to re-install every time you make a change.

If for any reason you don't want to use this approach, you can also run pfpgen from the root of the git
repository with either
```
$ python -m pfpgen <arguments...>
```
or using our wrapper script
```
$ ./pfpgenrun.py <arguments...>
```

## Contributing
If you'd like to contribute code back to `pfpgen`, please fork this github repository and send us a pull request!
Please make sure that your contribution passes our [continuous integration build](https://travis-ci.org/pfpsim/pfpgen).

# Support

If you need help using the PFPSim Framework, please
[send us an email at `pfpsim.help@gmail.com`](mailto:pfpsim.help@gmail.com) - we'd be happy to hear from you!

If you think you've found a bug, or would like to request a new feature,
[please open an issue using github](https://github.com/pfpsim/PFPSim/issues) - we're always trying to improve PFPSim!

# License

This project is licensed under the GPLv2 - see [`LICENSE`](/LICENSE) for details

# Authors
Copyright (C) 2016 Concordia Univ., Montreal
 - Samar Abdi
 - Umair Aftab
 - Gordon Bailey
 - Faras Dewal
 - Shafigh Parsazad
 - Eric Tremblay

Copyright (C) 2016 Ericsson
- Bochra Boughzala

