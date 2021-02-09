# This file is placed in the Public Domain.

from op.obj import Object, get
from op.hdl import Command

param = Object()
param.add = ["test@shell", "bart"]
param.dne = ["test4", ""]
param.edt = ["opbot.irc.Cfg",
             "opbot.irc.Cfg server=localhost",
             "opbot.irc.Cfg channel=#dunkbots"]
param.rm = ["reddit", ]
param.dpl = ["reddit title,summary,link",]
param.log = ["test1", ""]
param.flt = ["0", "1", ""]
param.fnd = ["cfg",
             "log",
             "todo",
             "cfg server==localhost",
             "rss rss==reddit rss",
             "email From==pvp From Subject -t"]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["test4", ""]
param.mbx = ["~/Desktop/25-1-2013", ""]

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
