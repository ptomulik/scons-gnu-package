#! /bin/sh

# Copyright (c) 2012 by Pawel Tomulik
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

# tools/update-libs.sh: update libraries in 'libs/' from internet repos.

set -e

SCRIPTDIR=$(dirname $(realpath $0))
TOPDIR=$(realpath ${SCRIPTDIR}/../)
SITEDIR=${TOPDIR}/site_scons
TMPDIR=/tmp
RMTMPDIR=false

# Create libs directory if doesn't exist
test -e ${SITEDIR} || mkdir ${SITEDIR}

#############################################################################
# download scons_docbook
DLDIR=$(mktemp -d --tmpdir=${TMPDIR})
TARBALL="${DLDIR}/scons_docbook.tar.gz"
URL='https://bitbucket.org/dirkbaechle/scons_docbook/get/default.tar.gz'
test -e ${SITEDIR}/site_tools/docbook || mkdir -p ${SITEDIR}/site_tools/docbook 
wget -O ${TARBALL} ${URL} && \
  (cd ${SITEDIR}/site_tools/docbook  && tar -xzf ${TARBALL} --wildcards --strip-components=1 '*scons_docbook*/__init__.py' '*scons_docbook*/utils')
rm -rf ${DLDIR}
#############################################################################
