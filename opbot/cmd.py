# This file is placed in the Public Domain.

import threading, time

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
