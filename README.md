SConsGnuPackage
===============

Welcome to SConsGnuPackage.

This package provides an easy way to define installable packages in your
scons-based project. It allows you to describe one or more packages that you
wish to create from your source tree and generate necessary scons targets
auto-magically. 

INSTALLATION
------------

Just copy entire directory ``SConsGnuPackage`` to your local ``site_scons``
directory. You'll also need additional packages to use ``SConsGnuPackage``.

DOWNLOADING DEPENDENCIES
------------------------

This package is not self-contained and have some external dependencies (see
[REQUIREMENTS](#requirements)). The first step after downloading the
``scons-gnu-package`` source tree is to download necessary dependencies.

### Downloading dependencies needed to use SConsGnuPackage

If you have th ``sh``-compatible shell, just run the 

    tools/download-user-deps.sh

script from the top-level source directrory. It will download necessary python
packages to ``site_scons`` directory. The script uses ``wget`` and ``tar``
programs.

### Downloading dependencies needed to develop SConsGnuPackage

If you have th ``sh``-compatible shell, just run the 

    tools/download-devel-deps.sh

script from the top-level source directrory.  The script uses ``wget`` and
``tar`` programs.


REQUIREMENTS
------------

### Packages that SConsGnuPackage depends on

The ``SConsGnuPackage`` needs following external packages to function properly:

  * ``SConsGnuVariables`` <https://github.com/ptomulik/scons-gnu-variables>

The ``SConsGnuVariables`` is installed by ``tools/download-user-deps.sh``.

### Software needed to generate documentation 

To generate user documentation you'll need:
  
  * ``docbook-xml`` <http://www.oasis-open.org/docbook/xml/>
  * ``xsltproc`` <ftp://xmlsoft.org/libxslt/>
  * ``scons_docbook`` tool <https://bitbucket.org/dirkbaechle/scons_docbook/overview>
    
The ``scons_docbook`` package is installed by ``tools/download-devel-deps.sh``.

To generate API documentation you'll need at least:

  * epydoc <http://epydoc.sourceforge.net/>
  * python-docutils <http://pypi.python.org/pypi/docutils>
  * python-pygments <http://pygments.org/>

Install these packages with your package manager.

DOCUMENTATION
-------------

### User's documentation

User's documentation may be generated with 

    scons user-doc

You'll find generated files under ``build/doc/user/``.

### API documentation

API documentation may be generated with 

    scons api-doc

You'll find generated files under ``build/doc/api/``.

LICENSE
-------

Copyright (c) 2012 by Pawel Tomulik

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
