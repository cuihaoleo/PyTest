#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# CheckFunctions.py
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

def LineCmp_StripEChar (srcfile, basefile, factor):
    def numiter ():
        i=1
        while True:
            yield i
            i += 1

    for line, src, base in \
            zip(numiter(), srcfile, basefile):
        if src.strip() != base.strip():
            return (0,
                     "输出文件差异！检查文件%s时，发现%d行与标准结果不同：\n"
                    "标准结果：%s\n"
                    "测试输出：%s" 
                    % (srcfile.name, line, src.strip(), base.strip()))

    for line in srcfile:
        if len(line.strip()):
            return (0,
                    "输出文件差异！检查文件%s时，发现文件过长。"
                    % srcfile.name)

    for line in basefile:
        if len(line.strip()):
            return (0,
                    "输出文件差异！检查文件%s时，发现文件过短。"
                    % srcfile.name)

    return (0, "")

DefaultChecker = LineCmp_StripEChar

