# OPLIB - Object Programming Library (test_tinder.py)
#
# This file is placed in the Public Domain.

import os, unittest

from op.bsc import Test
from op.obj import Object, get
from op.hdl import Command
from op.run import cfg
from op.thr import launch

from .prm import exec, param

events = []

class Test_Cmd(unittest.TestCase):

    def test_cmds(self):
        for x in range(cfg.index or 1):
            for cmd in h.cmds:
                events.extend(exec(cmd))

h = Test()
h.walk("opmod,opbot")
h.start()
