#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# ResultClass.py
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

import time
import threading

class record:
    pass

class PyTest_Result:
    def __init__ (self):
        self._score = 0
        self._time = ""
        self._memory = 0
        self._check = []
        self._failrec = ()
        self._rec = record()

    def TimingStart (self):
        self._time = time.time()

    def TimingEnd (self):
        self._time = time.time() - self._time

    def Fail (self):
        return bool(self._failrec)

    def FailRecord (self, binfile, retcode):
        self._failrec = (binfile, retcode)

    def MemoryWatch (self, pid):
        def watcher ():
            nonlocal pid
            while True:
                try:
                    mem = int(open("/proc/%d/statm" % pid). \
                            read().split()[1])
                except (IOError, OSError):
                    return
                else:
                    if mem > self._memory:
                        self._memory = mem
                    time.sleep(0.02)

        try:
            self._rec.memwatcher.join()
        except (AttributeError, NameError):
            pass
        finally:
            self._rec.memwatcher = threading.Thread(target=watcher)
            self._rec.memwatcher.start()

    def GetTime (self):
        if self._time < 1:
            return "%.2f ms" % (self._time*1000)
        elif self._time < 60:
            return "%.2f s" % self._time
        elif self._time < 3600:
            return "%.2f min" % (self._time/60)
        else:
            return "%.2f h" % (self._time/3600)

    def GetMemory (self):
        self._rec.memwatcher.join()
        if self._memory < 1024:
            return "%d Bytes" % self._memory
        elif self._memory < 1024*1024*4:
            return "%d KB" % (self._memory//1024)
        elif self._memory < 1024*1024*1024*4:
            return "%d MB" % (self._memory//(1024*1024))
        else:
            return "%d GB" % (self._memory//(1024*1024*1024))

    def AddResult (self, atfile, score, msg=""):
        self._score += score
        self._check.append({"file":atfile, "score":score, "msg":msg})

    def GetResult (self):
        return (x for x in self._check)

    def GetScore (self):
        return self._score

