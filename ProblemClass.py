#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# ProblemClass.py
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

import os
import shutil
import glob
import subprocess
import time
import CompileFunctions
import CheckFunctions
from ResultClass import PyTest_Result
from PyTestError import CompileError

class PyTest_Problem:
    def __init__ (self):
        self.Binary = []
        self.WorkDict = ""
        self.Record = []

        self.Name = "unname"
        self.Info = ""
        self.Compile = CompileFunctions.DefaultCompile
        self.Require = []

        self.Input = []
        self.Output = []

        self.CpuTime = self.Mem = None
        self.CheckFactor = 1.0
        self.CheckFunc = CheckFunctions.DefaultChecker

        self.PreExec = None

    def __del__ (self):
        if os.path.lexists(self.WorkDict):
            shutil.rmtree(self.WorkDict)

    def Reset (self):
        try:
            if os.path.lexists(self.WorkDict):
                shutil.rmtree(self.WorkDict)
        except (IOError, OSError):
            pass

    def AddInputData (self, data):
        self.Input.append(data)
    
    def AddOutputData (self, data):
        self.Output.append(data)

    def AddData (self, inp, oup):
        self.AddInputData(inp)
        self.AddOutputData(oup)

    def Prepare (self, srcpath):
        self.Reset()
        files = []
        for f in self.Require:
            if len(glob.glob(os.path.join(srcpath, f)))==0:
                raise CompileError("文件未找到", f)
            else:
                files.append(glob.glob(os.path.join(srcpath, f))[0])

        self.WorkDict, self.Binary = self.Compile(files)

    def Test (self):
        for finput, foutput in zip(self.Input, self.Output):
            fstdin = [None]*len(self.Binary)
            for ep, path in finput.items():
                if ep.startswith("@@"):
                    try:
                        fstdin[int(ep[2:])] = open(path)
                    except (ValueError, IndexError):
                        pass
                else:
                    shutil.copy2(path, os.path.join(self.WorkDict, ep))

            (result, stdout, stderr) = self.Exec(fstdin)
            if not result.Fail():
                self.Check(result, foutput, stdout, stderr)
            yield result

    def Exec (self, fstdin):
        rec = PyTest_Result()
        
        fstdout = [None]*len(self.Binary)
        fstderr = [None]*len(self.Binary)

        rec.TimingStart()
        for index, binfile in enumerate(self.Binary):
            proc = subprocess.Popen(binfile,
                                preexec_fn=self.PreExec,
                                cwd=self.WorkDict,
                                stdin=fstdin[index],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

            rec.MemoryWatch(proc.pid)
            proc.wait()

            fstdout[index] = proc.stdout
            fstderr[index] = proc.stderr

            if proc.returncode:
                rec.FailRecord(proc.returncode, binfile)
                break
        rec.TimingEnd()

        return (rec, fstdout, fstderr)

    def Check (self, result, foutput, stdout, stderr):
        ret = []

        for ep, path in foutput.items():
            if ep.startswith("@@"):
                try:
                    result.AddResult(ep, *self.CheckFunc(
                            stdout[int(ep[2:])],
                            open(path, "rb"),
                            self.CheckFactor
                        ))
                except (ValueError, IndexError):
                    result.AddResult(ep, 0)
            elif ep.startswith("@E"):
                try:
                    result.AddResult(ep, *self.CheckFunc(
                            stderr[int(ep[2:])],
                            open(path, "rb"),
                            self.CheckFactor
                        ))
                except (ValueError, IndexError):
                    result.AddResult(ep, 0)
            else:
                try:
                    result.AddResult(ep, *self.CheckFunc(
                            open(os.path.join(self.WorkDict,ep), "rb"),
                            open(path, "rb"),
                            self.CheckFactor
                        ))
                except (IOError, OSError):
                    result.AddResult(ep, 0, "输出文件未找到！")

