# This file is placed in the Public Domain.

from op.obj import get
from op.hdl import Command, Core
from op.run import cfg

from test.prm import param

class Test(Core):

    def direct(self, txt):
        if cfg.op("v"):
            print(txt)

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
    return res

def exec(cmd):
    exs = get(param, cmd, [""])
    e = list(exs)
    events = []
    nr = 0
    for ex in e:
        nr += 1
        txt = cmd + " " + ex
        e = Command(txt)
        h.put(e)
        events.append(e)
    return events

h = Test()
h.walk("opbot,opm,op")
h.start()
