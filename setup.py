# -*- coding: utf-8 -*-
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


"""setup.py: setuptools control."""

import re, os
from setuptools import setup, find_packages

try:
    version = os.environ["TRAVIS_TAG"]
    m = re.match("v(\d+\.\d+\.\d+)", version)
    if m:
        version = m.group(1)
    else:
        version = "0.0.0"
except KeyError:
    version = "0.0.0"

with open("pfpgen/version.py", "w") as version_file:
    version_file.write("__version__ = '%s'" % version)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "pfpgen",
    packages = find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"])+['pfpgen/templates'],
    include_package_data = True,
    entry_points = {
        "console_scripts": ['pfpgen = pfpgen.pfpgen:main']
        },
    version = version,
    description = "FAD Compiler",
    long_description = long_descr,
    author = "Samar Abdi",
    author_email = "pfpsim.help@gmail.com",
    keywords = "PFPGEN FAD SDN NPU P4 Dataplane 5G System",
    url = "pfpsim.github.io",
    install_requires=[
        'ply',
        'Tenjin',
        'pyyaml'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Debuggers",
    ],
    )
