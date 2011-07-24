#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# PyTestError.py
# This file is part of PyTest.
#
# PyTest
# Python编写的OI评测器后端
# Copyright (C) 2011  CUI Hao
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: 崔灏 (CUI Hao)
# Email: cuihao.leo@gmail.com
##

class CompileError (Exception):
    def __init__ (self, msg, filename, 
            cmd=None, retcode=None, stdout=None, stderr=None):
        self.msg = msg
        self.filename = filename
        self.cmd = cmd
        self.retcode = retcode
        self.stdout = stdout
        self.stderr = stderr

    def __str__ (self):
        return \
            "%s\n" % self.msg + \
            "FILE: %s\n" % self.filename + \
            "COMMAND: %s\n" % self.cmd + \
            "RETCODE: %s\n" % self.retcode + \
            "STDOUT: %s\n" % \
                (self.stdout.read() if self.stdout else None) + \
            "STDERR: %s" % \
                (self.stderr.read() if self.stderr else None)

class ConfigSyntaxError (Exception):
    def __init__ (self, msg, filename,
            section=None, option=None, value=None):
        self.msg = msg
        self.filename = filename
        self.section = section
        self.option = option
        self.value = value

    def __str__ (self):
        return \
            "%s\n" % self.msg + \
            "FILE: %s\n" % self.filename + \
            "SECTION: %s\n" % self.section + \
            "OPTION: %s\n" % self.option + \
            "VALUE: %s" % self.value

