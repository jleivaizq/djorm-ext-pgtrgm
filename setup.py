# -*- coding: utf-8 -*-
# Copyright (c) 2011 by Pablo Martín <goinnn@gmail.com>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="djorm-ext-pgtrgm",
    version="0.1",
    author="José Antonio Leiva",
    author_email="jleivaizq@gmail.com",
    description="Django application with some addons regarding PostgreSQL trigram text comparison",
    long_description=(read('README.md') + '\n\n' + read('CHANGES.rst')),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license="LGPL 3",
    keywords="django,querysets,lookup,pg_trgrm,similar,search",
    url='https://github.com/jleivaizq/djorm-ext-pgtrgm',
    packages=['djorm_pgtrgm'],
    include_package_data=True,
    zip_safe=False,
)
