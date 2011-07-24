#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# PlayerClass.py
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

def friendly_memory_view (memory):
    if memory <= 1024:
        return "%d Bytes" % memory
    memory = memory/1024
    if memory <= 1024:
        return "%.2f KB" % memory
    return "%.2f MB" % memory/1024

class PyTest_Player:
    def __init__ (self, dic, name=None):
        self.Path = os.path.abspath(dic)
        self.Record = {}
        self.Score = {}
        if name:
            self.Name = name
        else:
            self.Name = os.path.basename(self.Path)

    def Do (self, prob):
        print("被测试者：%s (%s)" % (self.Name, self.Path))
        print("题目：%s" % prob.Name)

        prob.Reset()
        self.Record[prob.Name]={}
        score = 0.0
        try:
            prob.Prepare(self.Path)
        except Exception as err:
            print("    编译错误，测试中止")
            self.Record[prob.Name]["prepare"] = \
                    [{"file":"SRC", "msg":err, "score":0}]
        else:
            for index, item in enumerate(prob.Test()):
                print("  #测试点 %s" % index)
                self.Record[prob.Name][index] = item
                score += item.GetScore()
                for chk in item.GetResult():
                    print("    > 检查 %s... " 
                            % chk["file"][:12].ljust(12), end='')
                    print("得分：%g" % chk["score"])
                print("    内存峰值：%s" % item.GetMemory())
                print("    运行时间：%s" % item.GetTime())

        print("总得分：%g" % score)
        self.Score[prob.Name] = score

