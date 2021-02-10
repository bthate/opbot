# This file is placed in the Public Domain.

import threading
import time

from op.dbs import last
from op.hdl import Bus
from op.obj import Cfg, format, keys, save, update

from .usr import User

def __dir__():
    return ("cmd", "cfg", "dlt", "met")

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))

def cfg(event):
    from .irc import Cfg
    c = Cfg()
    last(c)
    if event.prs and not event.prs.sets:
        return event.reply(format(c, skip=["username", "realname"]))
    update(c, event.prs.sets)
    save(c)
    event.reply("ok")

def dlt(event):
    if not event.args:
        return
    selector = {"user": event.args[0]}
    for fn, o in find("opmod.usr.User", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break

def met(event):
    if not event.args:
        return
    u = User()
    u.user = event.rest
    u.perms = ["USER"]
    save(u)
    event.reply("ok")
