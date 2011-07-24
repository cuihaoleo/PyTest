#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# CompileFunctions.py
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

def DefaultCompile (files):
    from PyTestError import CompileError
    import os
    import tempfile
    import subprocess
    import shlex

    wkdict = tempfile.mkdtemp()

    cmds = {
            ".c":   ("gcc -O0 {src} -o {exe}", "./{exe}"),
            ".cpp": ("g++ -O0 {src} -o {exe}", "./{exe}"),
            ".pas": ("fpc -O0 {src} -o {exe}", "./{exe}"),
            ".py":  ("", "python {src}"),
            ".exe": ("", "{src}")
        }

    ret = []
    for f in files:
        try:
            cmd = cmds[os.path.splitext(f)[-1]]
        except KeyError:
            raise CompileError("未知文件格式。", f)

        binfile = os.path.basename(f)+".exe"
        cpl = cmd[0].format(src=f, exe=os.path.join(wkdict, binfile))
        if len(cpl) > 0:
            try:
                p = subprocess.Popen(
                        shlex.split(cpl),
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE
                    )
            except OSError:
                raise CompileError("编译器未找到。", f, cmd=cpl)

            p.wait()
            if p.poll():
                raise CompileError("编译失败。", f, 
                            cmd = cpl,
                            retcode = p.returncode,
                            stdout = p.stdout,
                            stderr = p.stderr)

            if not os.path.lexists(os.path.join(wkdict, binfile)):
                raise CompileError("可执行文件未找到。", f, 
                            cmd = cpl,
                            retcode = p.returncode,
                            stdout = p.stdout,
                            stderr = p.stderr)

        ret.append(cmd[1].format(src=f, exe=binfile).split())

    return (wkdict, ret)

