#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# ProblemConfig.py
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
import configparser as CP
import sys
import CompileFunctions
import CheckFunctions
import glob
from ProblemClass import PyTest_Problem
from PyTestError import ConfigSyntaxError
import resource

def LimitIt (cputime=None, mem=None):
    def retfunc ():
        if cputime:
            resource.setrlimit(resource.RLIMIT_CPU, (cputime,cputime))  
        if mem:
            resource.setrlimit(resource.RLIMIT_AS, (mem,mem))
        return retfunc
                                                                    

def Cfg2Prob (cfgfile):
    if not os.path.isfile(cfgfile):
        raise ConfigSyntaxError("文件未找到。", cfgfile)

    prob = PyTest_Problem()

    config = CP.ConfigParser()
    config.read(cfgfile)
    rootpath = os.path.dirname(os.path.abspath(cfgfile))
    sys.path.append(rootpath)

    # Section Info
    if config.has_section("Info"):
        prob.Name = config["Info"].get("Name", "Unnamed")
        prob.Info = config["Info"].get("Info", "")

    # Section Source
    if config.has_section("Source"):
        mod = config["Source"].get("ImportModule", "")
        func = config["Source"].get("Compile")
        try:
            prob.Compile = getattr(__import__(mod), func)
        except (ImportError, AttributeError, ValueError):
            prob.Compile = getattr(CompileFunctions, func)

        for gl in config["Source"].get("Require", "").split():
            prob.Require.append(gl)

    # Section Input
    inp = []
    if config.has_section("Input"):
        for ep, path in config["Input"].items():
            for index, f in enumerate(sorted(glob.glob(os.path.join(rootpath, path)))):
                try:
                    inp[index][ep] = f
                except IndexError:
                    inp.append({ep:f})

    # Section Output
    oup = []
    if config.has_section("Output"):
        for ep, path in config["Output"].items():
            for index, f in enumerate(sorted(glob.glob(os.path.join(rootpath, path)))):
                try:
                    oup[index][ep] = f
                except IndexError:
                    oup.append({ep:f})

    for i, o in zip(inp, oup):
        prob.AddData(i, o)

    # Section Execute
    cputime = mem = None
    if config.has_section("Execute"):
        try:
            cputime = \
                config["Execute"].getfloat("TimeLimitSec", 0.0)
        except ValueError:
            raise ConfigSyntaxError \
                    ("数字不可识别。", cfgfile, 
                        "Execute", "TimeLimitSec", 
                        config["Execute"].get("TimeLimitSec"))
        try:
            mem = \
                config["Execute"].getfloat("MemoryLimitKB", 0.0)*1024
        except ValueError:
            raise ConfigSyntaxError \
                    ("数字不可识别。", cfgfile,
                        "Execute", "MemoryLimitKB",
                        config["Execute"].get("MemoryLimitKB"))
    prob.PreExec = LimitIt(cputime, mem)

    # Section Check
    if config.has_section("Check"):
        mod = config["Check"].get("ImportModule", "")
        func = config["Check"].get("Function")
        prob.CheckFactor = config["Check"].getfloat("Factor", 1.0)
        try:
            prob.CheckFunc = getattr(__import__(mod), func)
        except (ImportError, AttributeError, ValueError):
            prob.CheckFunc = getattr(CheckFunctions, func)

    return prob

