"""`SConsGnuPackage.Install`

Installation procedures for user defined software packages.
"""

#
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

__docformat__ = "restructuredText"

def _install_dest_common(env, pkg, uname2, source, **kw):
    from os import path
    from SConsGnuVariables.AmUniformNames import RSplitMainPrefix
    from SConsGnuPackage.Control import GnuPkgName
    prefix, primary = uname2
    prefix_ = prefix + '_'
    if prefix_.find('nobase_') >= 0:
        cwd = env.fs.getcwd().get_abspath()    
        relpath = path.relpath(source.get_abspath(), cwd)
    else:
        relpath = path.basename(source.get_abspath())
    add_prefix, main_prefix = RSplitMainPrefix(prefix,**kw)
    dir_var = '$' + main_prefix + 'dir'
    if main_prefix in ('data', 'libexec', 'pkgdata', 'pkginclude', 'pkglib', \
                      'pkglibexec'):
        pkg_name = GnuPkgName(env, pkg,**kw)
        dir_base = path.join(env.subst(dir_var), pkg_name)
    elif main_prefix == 'doc':
        pkg_name = GnuPkgName(env,pkg,**kw)
        # FIXME: pkg_name suffix shall include version string?
        dir_base = env.subst(dir_var)
    elif main_prefix == 'locale':
        pkg_name = GnuPkgName(env,pkg,**kw)
        basename, ext = path.splitext(path.basename(source.get_abspath()))
        dir_base = path.join(env.subst(dir_var), basename)
        relpath = pkg_name + ext
    else:
        dir_base = env.subst(dir_var)
    return dir_base, relpath

def _default_install_dest(env, pkg, uname2, source, **kw):
    from os import path
    dir_base, relpath = _install_dest_common(env, pkg, uname2, source, **kw)
    return path.join(dir_base, relpath)

def _program_install_dest(env, pkg, uname2, source, **kw):
    from os import path
    dir_base, relpath = _install_dest_common(env, pkg, uname2, source, **kw)
    prefix_ = uname2[0] + '_'
    if prefix_.find('notrans_') == -1:
        relprefix, basename = path.split(relpath)
        if env.has_key('program_prefix'):
            program_prefix = env['program_prefix']
        else:
            program_prefix = ''
        if env.has_key('program_suffix'):
            program_suffix = env['program_suffix']
        else:
            program_suffix = ''
        if env.has_key('program_transform'):
            program_transform = env['program_transform']
        else:
            program_transform = ''
        # FIXME: for program_transform we need to run sed somehow
        #        it is also unclear if we should transform relpath
        #        or program_prefix + relpath + program_suffix
        if program_transform:
            raise NotImplementedError('--program-transform is not supported')
        basename = program_prefix + basename + program_suffix
        relpath = path.join(relprefix, basename)
    return path.join(dir_base, relpath)

def _man_install_dest(env, pkg, uname2, source, **kw):
    from os import path
    from SConsGnuVariables.AmUniformNames import RSplitMainPrefix, \
                                                 StandardManSections
    prefix, primary = uname2
    prefix_ = prefix + '_'
    if prefix_.find('nobase_') >= 0:
        raise ValueError("illegal 'nobase_' prefix in %r" \
                         % prefix + '_' + primary)
    add_prefix, main_prefix = RSplitMainPrefix(prefix,**kw)
    # FIXME: what if main_prefix is None?
    std_sections = StandardManSections(**kw)
    if len(main_prefix) >= 4:
        dp_sec = main_prefix[3]
        if dp_sec not in std_sections:
            raise ValueError("non-standard man section in %r" \
                            % prefix + '_' + primary)
    else:
        dp_sec = None
    # Split filename onto basename and extension
    basename, ext = path.splitext(path.basename(source.get_abspath()))
    # Try to determine man section encoded in file extension
    if len(ext) >= 2: 
        ext_sec = ext[1]
        if ext_sec not in std_sections:
            ext_sec = None
    else:
        ext_sec = None
    # Determine what is the destination man section
    if dp_sec is None:
        if ext_sec is None:
            raise RuntimeError("can't determine man section for %s=%s" \
                             % (prefix + '_' + primary, str(source)))
        else:
            sec = ext_sec
    else:        
        sec = dp_sec
    # Determine if and how to change extension of the installed file
    if prefix_.find('notrans_') == -1:
        if ((ext_sec is not None) and (ext_sec == sec)):
            dst_ext = ext
        else:
            dst_ext = env.subst('${man'+sec+'ext}')
    else:
        dst_ext = ext
    # Choose main_prefix containing man section
    if dp_sec is None:
        main_prefix = 'man' + sec
    dir_base, relpath = _install_dest_common(env, pkg, uname2, source, **kw)
    return path.join(dir_base, basename + dst_ext)
    
def _install_multi(env, pkg, uname2, sources, destfun, *args, **kw):
    targets = []
    for source in sources:
        dest = destfun(env, pkg, uname2, source, **kw)
        target = env.InstallAs(dest, source)
        targets.extend(target)
    return targets

def _install_PROGRAMS(env, pkg, uname2, sources, *args, **kw):
    destfun = _program_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_LIBRARIES(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_LTLIBRARIES(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_LISP(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_PYTHON(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_JAVA(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_SCRIPTS(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_DATA(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_HEADERS(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_MANS(env, pkg, uname2, sources, *args, **kw):
    destfun = _man_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_TEXINFOS(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)

def _install_LOCALES(env, pkg, uname2, sources, *args, **kw):
    destfun = _default_install_dest
    return _install_multi(env, pkg, uname2, sources, destfun, *args, **kw)


__standard_install_handlers = {
    'PROGRAMS'      : _install_PROGRAMS,
    'LIBRARIES'     : _install_LIBRARIES,
    'LTLIBRARIES'   : _install_LTLIBRARIES,
    'LISP'          : _install_LISP,
    'PYTHON'        : _install_PYTHON,
    'JAVA'          : _install_JAVA,
    'SCRIPTS'       : _install_SCRIPTS,
    'DATA'          : _install_DATA,
    'HEADERS'       : _install_HEADERS,
    'MANS'          : _install_MANS,
    'TEXINFOS'      : _install_TEXINFOS,
    'LOCALES'       : _install_LOCALES,
}

def _install_group(env, pkg, uname, sources, *args, **kw):
    from SCons.Util import flatten, is_String
    from SConsGnuVariables.AmUniformNames import RSplitPrimaryName
    prefix, primary = RSplitPrimaryName(uname,**kw)
    if primary is None:
        raise ValueError('malformed uniform name: %s' % uname)
    try:
        handler = __standard_install_handlers[primary]
    except KeyError:
        # FIXME: default install handler?
        handler = None
    sources = env.arg2nodes(sources)
    sources = flatten(sources)
    return handler(env, pkg, (prefix,primary), sources, *args, **kw)

def _install_groups(env, pkg, unames, *args, **kw):
    targets = []
    try:
        content = pkg['content']
    except KeyError:
        return targets
    # select only the requested unames for installation
    content = dict(filter(lambda x : x[0] in unames, content.iteritems()))
    for uname, source in content.iteritems():
        targets.extend(_install_group(env, pkg, uname, source, *args, **kw))
    return targets

def _env_override(env, pkg, *args, **kw):
    from SConsGnuPackage.Control import GnuPkgName
    overrides = {}
    overrides['install_package'] =  GnuPkgName(env,pkg,**kw) 
    return env.Override(overrides)


def GnuPkgInstallExec(env, pkg, *args, **kw):
    from SConsGnuVariables.AmUniformNames import FilterInstallExecNames
    env = _env_override(env,pkg,*args,**kw)
    try:
        # extract only the entries that should be installed as install-exec
        unames = FilterInstallExecNames(pkg['content'].keys())
    except KeyError:
        return []
    return _install_groups(env, pkg, unames, *args, **kw)


def GnuPkgInstallData(env, pkg, *args, **kw):
    from SConsGnuVariables.AmUniformNames import FilterInstallDataNames
    env = _env_override(env,pkg,*args,**kw)
    try:
        # extract only the entries that should be installed as install-exec
        unames = FilterInstallDataNames(pkg['content'].keys())
    except KeyError:
        return []
    return _install_groups(env, pkg, unames, *args, **kw)

def GnuPkgInstallExecAndData(env, pkg, *args, **kw):
    return GnuPkgInstallExec(env, pkg, *args, **kw) \
        +  GnuPkgInstallData(env, pkg, *args, **kw)
    
# Local Variables:
# # tab-width:4
# # indent-tabs-mode:nil
# # End:
# vim: set syntax=python expandtab tabstop=4 shiftwidth=4:
