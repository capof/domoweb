#!/usr/bin/python
# -*- coding: utf-8 -*-

""" This file is part of B{Domogik} project (U{http://www.domogik.org}).

License
=======

B{Domogik} is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

B{Domogik} is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Domogik. If not, see U{http://www.gnu.org/licenses}.

Module purpose
==============

Help to manage DomoWeb installation

Implements
==========


@author: Domogik project
@copyright: (C) 2007-2009 Domogik project
@license: GPL(v3)
@organization: Domogik
"""

import ez_setup
ez_setup.use_setuptools()

import os
from setuptools import setup, find_packages
import platform

def list_all_files(path, dst):
    """
    List all files and subdirectories contained in a path
    @param path : the path from where to get files and subdirectories
    @param dst : The based destination path
    @return : a list of tuples for each directory in path (including path itself)
    """
    d = []
    files = []
    for i in os.listdir(path):
        if not os.path.isdir(os.path.join(path, i)):
            files.append(os.path.join(path, i))
        else:
            d.extend(list_all_files(os.path.join(path, i), os.path.join(dst, i)))
    d.append((dst, files))
    return d

arch = platform.architecture()

d_files = [
        ('/etc/init.d/', ['src/domogik/examples/init/domoweb']),
        ('/etc/default/', ['src/domogik/examples/default/domoweb'])
]

d_files.extend(list_all_files('src/domoweb/home/templates/', '/usr/local/share/domoweb/home/templates/')),
d_files.extend(list_all_files('src/domoweb/admin/templates/', '/usr/local/share/domoweb/admin/templates/')),
d_files.extend(list_all_files('src/domoweb/view/templates/', '/usr/local/share/domoweb/view/templates/')),
d_files.extend(list_all_files('src/domoweb/locale/', '/usr/local/share/domoweb/locale/')),
d_files.extend(list_all_files('src/domoweb/apache/', '/usr/local/share/doc/domoweb/examples/apache/')),

setup(
    name = 'DomoWeb',
    version = '0.2.0',
    url = 'http://www.domogik.org/',
    description = 'Domogik Web UI',
    author = 'Domogik team',
    author_email = 'domogik-general@lists.labs.libre-entreprise.org',
    install_requires=['setuptools', 
                      'django < 1.3',
                      'simplejson >= 1.9.2',
                      'httplib2 >= 0.6.0', 
                      'django-pipes >= 0.2', 
                      'Distutils2'],
    zip_safe = False,
    license = 'GPL v3',
    # namespace_packages = ['domogik', 'mpris', 'tools'],
    # include_package_data = True,
#    packages = find_packages('src', exclude=["mpris"]),
    package_dir = {'': 'src'},
#    test_suite = 'domogik.tests',
    # Include all files of the ui/djangodomo directory
    # in data files.
    package_data = {
        'domoweb': list_all_files('src/domoweb/','.')[0][1],
        'domoweb': ['locale/*.po', 'locale/*.mo'],
#        'domogik.ui.djangodomo.core': list_all_files('src/domogik/ui/djangodomo/core/templates/'),
    },
    data_files = d_files,

    entry_points = {
        'console_scripts': [
            """
            dmg_domoweb = domoweb.manage:run_manager
            """
        ],
    },
)