# This file is placed in the Public Domain.

import threading
import time

from op.dbs import last
from op.hdl import Bus
from op.obj import Cfg, format, keys, save, update

from .usr import User

def __dir__():
    return ("cmd",)

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))

def dlt(event):
    if not event.args:
        return
    selector = {"user": event.args[0]}
    for fn, o in find("opbot.usr.User", selector):
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
