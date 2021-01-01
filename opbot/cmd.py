# OPBOT - operbot (cmd.py)
#
# this file is placed in the public domain

"commands (cmd)"

# imports

import ol
import threading
import time

# defines

def __dir__():
    return ("Log", "Todo", "cmd", "cfg", "dpl", "dne", "flt", "fnd", "ftc", "log", "rem", "rss", "tdo", "thr", "ver")

starttime = time.time()

# classes

class Log(op.Object):

    "log items"

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(op.Object):

    "todo items"

    def __init__(self):
        super().__init__()
        self.txt = ""

# commands

def cmd(event):
    "list commands (cmd)"
    bot = op.hdl.Bus.by_orig(event.orig)
    if bot:
        c = sorted(op.keys(bot.cmds))
        if c:
            event.reply(",".join(c))

def cfg(event):
    "configure irc (cfg)"
    c = op.irc.Cfg()
    op.dbs.last(c)
    if not event.prs.sets:
        return event.reply(op.format(c, skip=["username", "realname"]))
    op.update(c, event.prs.sets)
    op.save(c)
    event.reply("ok")


def dne(event):
    "flag as done (dne)"
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for fn, o in op.dbs.find("op.cmd.Todo", selector):
        o._deleted = True
        op.save(o)
        event.reply("ok")
        break

def dpl(event):
    "set keys to display (dpl)"
    if len(event.args) < 2:
        return
    setter = {"display_list": event.args[1]}
    for fn, o in op.dbs.last_match("op.rss.Rss", {"rss": event.args[0]}):
        op.edit(o, setter)
        op.save(o)
        event.reply("ok")

def flt(event):
    "list of bots"
    try:
        event.reply(str(op.hdl.Bus.objs[event.prs.index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(",".join([op.get_name(o) for o in op.hdl.Bus.objs]))

def fnd(event):
    "find objects (fnd)"
    if not event.args:
        fls = op.dbs.list_files(op.wd)
        if fls:
            event.reply(" | ".join([x.split(".")[-1].lower() for x in fls]))
        return
    nr = -1
    for otype in op.get(op.tbl.names, event.args[0], [event.args[0]]):
        for fn, o in op.dbs.find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), op.format(o, event.xargs or op.keys(o), skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (op.prs.elapsed(time.time() - op.utl.fntime(fn)))
            event.reply(txt)
            
def ftc(event):
    "run a fetch (ftc)"
    res = []
    thrs = []
    fetcher = op.rss.Fetcher()
    fetcher.start(False)
    thrs = fetcher.run()
    for thr in thrs:
        res.append(thr.join() or 0)
    if res:
        event.reply("fetched %s" % ",".join([str(x) for x in res]))
        return

def log(event):
    "log some text (log)"
    if not event.rest:
        return
    l = Log()
    l.txt = event.rest
    op.save(l)
    event.reply("ok")

def rem(event):
    "remove a rss feed (rem)"
    if not event.args:
        return
    selector = {"rss": event.args[0]}
    nr = 0
    got = []
    for fn, o in op.dbs.find("op.rss.Rss", selector):
        nr += 1
        o._deleted = True
        got.append(o)
    for o in got:
        op.save(o)
    event.reply("ok")

def rss(event):
    "add a rss feed (rss)"
    if not event.args:
        return
    url = event.args[0]
    res = list(op.dbs.find("op.rss.Rss", {"rss": url}))
    if res:
        return
    o = op.rss.Rss()
    o.rss = event.args[0]
    op.save(o)
    event.reply("ok")

def tdo(event):
    "add a todo item (tdo)"
    if not event.rest:
        return
    o = Todo()
    o.txt = event.rest
    op.save(o)
    event.reply("ok")

def thr(event):
    "list running threads (thr)"
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = op.Object()
        op.update(o, thr)
        if op.get(o, "sleep", None):
            up = o.sleep - int(time.time() - o.state.latest)
        else:
            up = int(time.time() - starttime)
        thrname = thr.getName()
        if not thrname:
            continue
        if thrname:
            result.append((up, thrname))
    res = []
    for up, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s %s" % (txt, op.prs.elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def ver(event):
    "show version (ver)"
    event.reply("OLIB %s - pure python3 object library" % op.__version__)
