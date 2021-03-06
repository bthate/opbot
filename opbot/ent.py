# OPBOT - pure python3 IRC bot (bin/clean)
#
# This file is placed in the Public Domain.

"entry"

# imports

from op.dbs import find
from op.obj import Object, save

# classes

class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

# commands

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("opbot.ent.Todo", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def log(event):
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    save(l)
    event.reply("ok")

def tdo(event):
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")
