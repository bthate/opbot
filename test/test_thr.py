# OPLIB - Object Programming Library (test_tinder.py)
#
# This file is placed in the Public Domain.

import os, unittest

from op.bsc import Test
from op.obj import Object, get
from op.hdl import Command, Handler, cmd
from op.run import cfg
from op.thr import launch

from .prm import execute, param

events = []

class Test_Tinder(unittest.TestCase):

    def test_thrs(self):
        thrs = []
        for x in range(cfg.index or 1):
            launch(tests, h)
        consume(events)

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

def tests(b):
    for cmd in h.cmds:
        events.extend(exec(cmd))

h = Test()
h.walk("opmod,opbot")
h.start()
