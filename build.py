#   yadtcontroller
#   Copyright (C) 2013 Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
from pybuilder.core import use_plugin, init, Author

use_plugin('python.core')
use_plugin('python.install_dependencies')

use_plugin('filter_resources')
use_plugin('copy_resources')

use_plugin('python.coverage')
use_plugin('python.distutils')
use_plugin('python.unittest')
use_plugin('python.distutils')
use_plugin('python.flake8')

authors = [Author('Marcel Wolf', 'marcel.wolf@immobilienscout24.de'),
           Author('Maximilien Riehl', 'maximilien.riehl@gmail.com'),
           Author('Michael Gruber', 'aelgru@gmail.com')]
license = 'GNU GPL v3'
name = 'yadtcontroller'
url = 'https://github.com/yadt/yadtcontroller'
version = '0.1.0'

default_task = ['analyze', 'publish']


@init
def set_properties(project):
    project.build_depends_on('mockito')
    project.build_depends_on('flake8')
    project.build_depends_on('mock')

    project.depends_on('docopt')
    project.depends_on('yadtcommons')
    project.depends_on('yadtbroadcast-client')
    project.depends_on('Twisted')
    project.depends_on('fysom')

    project.get_property('filter_resources_glob').append('**/yadt_controller/__init__.py')
    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')


@init(environments="teamcity")
def set_properties_for_teamcity(project):
    import os
    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_build_dependencies', 'package']
    project.get_property('distutils_commands').append('bdist_rpm')
