# OP - Object Programming Lirbrary (cmd.py)
#
# this file is placed in the Public Domain

import op

class Log(op.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(op.Object):

    def __init__(self):
        super().__init__()
        self.txt = ""

def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in find("mod.ent.Todo", selector):
        o._deleted = True
        op.save(o)
        event.reply("ok")
        break

def log(event):
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    op.save(l)
    event.reply("ok")

def tdo(event):
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    op.save(o)
    event.reply("ok")
