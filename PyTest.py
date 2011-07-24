#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##
# PyTest.py
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

import cmd
import os
import shlex
import pickle
from PlayerClass import PyTest_Player
from ProblemClass import PyTest_Problem
from ProblemConfig import Cfg2Prob

class PyTest_Cmd (cmd.Cmd):
    def __init__ (self):
        cmd.Cmd.__init__(self)
        self.prompt = "(PyTest) "
        self.Name = "Unnamed"
        self.Players = {}
        self.Problems = {}
        self.do_EOF = self.do_quit

    def AddProb (self, cfg):
        try:
            prob = Cfg2Prob(cfg)
        except Exception as exp:
            print("无法添加题目 %s ： 导入时发生错误")
            print(exp)
        else:
            if prob.Name in self.Problems.keys():
                print("无法添加题目 %s ： 相同名称的题目已存在" % prob.Name)
            else:
                self.Problems[prob.Name] = prob
                print("添加题目 %s" % prob.Name)

    def AddPlayer (self, path):
        try:
            player = PyTest_Player(path)
        except Exception as exp:
            print("无法添加选手 %s ： 导入时发生错误")
            print(exp)
        else:
            if player.Name in self.Players.keys():
                print("无法添加选手 %s ： 相同名称的对象已存在" % player.Name)
            else:
                self.Players[player.Name] = player
                print("添加选手 %s" % player.Name)

    def DelProb (self, name):
        try:
            del self.Problems[name]
        except KeyError:
            print("无法删除题目 %s ： 题目不存在" % name)
        else:
            print("删除题目 %s" % name)

    def DelPlayer (self, name):
        try:
            del self.Players[name]
        except KeyError:
            print("无法删除选手 %s ： 对象不存在" % name)
        else:
            print("删除选手 %s" % name)

    def Testit (self, pl, pr):
        try:
            player = self.Players[pl]
        except KeyError:
            print("未知用户 %s" % pl)
            return

        try:
            prob = self.Problems[pr]
        except KeyError:
            print("未知用户 %s" % pr)
            return

        player.Do(prob)
        
    def help_quit (self):
        print("quit")
        print("退出")
    def do_quit (self, line):
        exit()

    def help_name (self):
        print("name [@名称]")
        print("设置评测名称。若没有提供，显示当前名称")
    def do_name (self, name):
        if len(name.strip()) == 0:
            print(self.Judge.Name)
        else:
            self.Judge.Name = name

    def help_addprob (self):
        print("addprob @配置文件1 [@配置文件2 [...]]")
        print("添加题目")
    def do_addprob (self, line):
        for path in shlex.split(line):
            self.AddProb(path)

    def help_delprob (self):
        print("delprob @题目1 [@题目2 [...]]")
        print("删除题目")
    def do_delprob (self, line):
        for name in shlex.split(line):
            self.DelProb(name)

    def help_prob (self):
        print("prob")
        print("显示所有题目")
    def do_prob (self, line):
        for p in self.Problems:
            print("%s: %s" % (p, self.Problems[p].CfgFile))

    def help_add (self):
        print("add @目录1 [@目录2 [...]]")
        print("添加选手")
    def do_add (self, line):
        for path in shlex.split(line):
            self.AddPlayer(path)

    def help_addall (self):
        print("addall @目录1 [@目录2 [...]]")
        print("添加目录中的所有文件夹作为选手")
    def do_addall (self, line):
        for path in shlex.split(line):
            try:
                paths = next(os.walk(path))[1]
            except StopIteration:
                continue

            for f in paths:
                self.AddPlayer(os.path.join(path, f))

    def help_del (self):
        print("del @选手1 [@选手2 [...]]")
        print("删除选手")
    def do_del (self, line):
        for name in shlex.split(line):
            self.DelPlayer(name)

    def help_player (self):
        print("player")
        print("显示所有选手")
    def do_player (self, line): 
        for p in self.Players:
            print("%s: %s" % (p, self.Players[p].Path))

    def help_rec (self):
        print("rec @选手 @题目")
        print("显示详细评测信息")
    def do_rec (self, line):
        arg = shlex.split(line)
        if len(arg)==2:
            pl, pr = arg
        else:
            return

        try:
            li = self.Players[pl].Record[pr]
        except KeyError:
            print("记录不存在")
            return

        for idx in li:
            print()
            print("[测试#%s]" % idx)

            for dic in li[idx]:
                print("<文件 %s>" % dic.get("file", ""))
                print("信息： %s" % dic.get("msg", ""))
                print("得分： %s" % dic.get("score", ""))

    def help_print (self):
        print("打印Python表达式")
    def do_print (self, line):  
        try:
            print(eval(line))
        except Exception as err:
            print(err)

    def help_test (self):
        print("启动测试")
    def do_test (self, line):
        arg = shlex.split(line)

        if len(arg) == 2:
            Testit(*arg)
        elif len(arg) == 0:
            pls = input("测试对象（默认全部）：").split()
            prs = input("题目（默认全部）：").split()

            if len(pls) == 0:
                pls = self.Players.keys()
            if len(prs) == 0:
                prs = self.Problems.keys()

            for player in pls:
                for prob in prs:
                    self.Testit(player, prob)
                print()

    def help_save (self):
        print("储存本次测试")
    def do_save (self, line):
        path = shlex.split(line)[0]
        if os.path.lexists(path):
            while True:
                ch = input("文件已存在，是否覆盖(Y/N)？")
                if ch in ("y", "Y"):
                    break
                elif ch in ("n", "N"):
                    return

        f = open(path, "wb")
        pickle.dump(self.Name, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.Players, f, pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.Problems, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    def help_load (self):
        print("加载测试")
    def do_load (self, line):
        path = shlex.split(line)[0]

        try:
            f = open(path, "rb")
        except IOError as err:
            print(err)
            return

        self.Name = pickle.load(f)
        self.Players = pickle.load(f)
        self.Problems = pickle.load(f)

if __name__ == '__main__':
    pytest = PyTest_Cmd()
    pytest.cmdloop()

