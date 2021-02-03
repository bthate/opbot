# OPLIB - Object Programming Library (test_tinder.py)
#
# This file is placed in the Public Domain.

import os
import random
import sys
import unittest

sys.path.insert(0, os.getcwd())

from op.obj import Object, get
from op.hdl import Command, Handler, cmd
from op.prs import parse_cli
from op.run import cfg
from op.thr import launch

param = Object()
param.add = ["test@shell", "bart"]
param.dne = ["test4", ""]
param.edt = ["operbot.rss.Cfg", "operbot.rss.Cfg server=localhost", "operbot.rss.Cfg channel=#dunkbots"]
param.rm = ["reddit", ]
param.dpl = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg", "log", "todo", "cfg server==localhost", "rss rss==reddit rss", "email From==pvp From Subject -t"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.mbx = ["~/Desktop/25-1-2013", ""]

events = []
ignore = ["mbx", "rss"]
nrtimes = 1

# classes

class TestHandler(Handler):

    def direct(self, txt):
        if cfg.verbose:
            print(txt)

class Command(Command):

    def __str__(self):
        return self.txt

    def direct(self, txt):
        if cfg.verbose:
            print(txt)

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            launch(tests, h)
        consume(events)

    def test_neuman(self):
        for x in range(cfg.index or 1):
            tests(h)

    def test_sorted(self):
        for x in range(cfg.index or 1):
            sortedtests(h)

def consume(elems):
    fixed = []
    res = []
    for e in elems:
        r = e.wait()
        res.append(r)
        fixed.append(e)
    for f in fixed:
        try:
            elems.remove(f)
        except ValueError:
            continue
    h.stop()
    return res

def sortedtests(b):
    keys = sorted(h.cmds)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def tests(b):
    keys = list(h.cmds)
    random.shuffle(keys)
    for cmd in keys:
        if cmd in ignore:
            continue
        events.extend(do_cmd(cmd))

def do_cmd(cmd):
    exs = get(param, cmd, [""])
    e = list(exs)
    random.shuffle(e)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex
        e = Command(txt)
        h.put(e)
        events.append(e)
    return events

h = TestHandler()
h.register("cmd", cmd)
h.load("op.cmd")
h.walk("opmod")
h.start()
