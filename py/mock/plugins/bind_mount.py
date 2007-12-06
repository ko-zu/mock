# vim:expandtab:autoindent:tabstop=4:shiftwidth=4:filetype=python:textwidth=0:
# License: GPL2 or later see COPYING
# Written by Michael Brown
# Copyright (C) 2007 Michael E Brown <mebrown@michaels-house.net>

# python library imports
import os

# our imports
from mock.trace_decorator import decorate, traceLog, getLog

import mock.util

requires_api_version = "1.0"

# plugin entry point
decorate(traceLog())
def init(rootObj, conf):
    BindMount(rootObj, conf)

# classes
class BindMount(object):
    """bind mount dirs from host into chroot"""
    decorate(traceLog())
    def __init__(self, rootObj, conf):
        self.rootObj = rootObj
        self.bind_opts = conf
        self.rootdir = rootObj.rootdir
        rootObj.bindMountObj = self
        rootObj.addHook("preinit",  self._bindMountPreInitHook)
        for srcdir, destdir in self.bind_opts['dirs']:
            rootObj.umountCmds.append('umount -n %s/%s' % (rootObj.rootdir, destdir))
            rootObj.mountCmds.append('mount -n --bind %s  %s/%s' % (srcdir, rootObj.rootdir, destdir))

    decorate(traceLog())
    def _bindMountPreInitHook(self):
        for srcdir, destdir in self.bind_opts['dirs']:
            mock.util.mkdirIfAbsent("%s/%s" % (self.rootObj.rootdir, destdir))