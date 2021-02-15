# OPBOT - pure python3 IRC bot (opbot/cmd.py)
#
# This file is placed in the Public Domain.

"list of commands"

# imports

import threading, time

from op.dbs import last
from op.hdl import Bus
from op.obj import Cfg, format, keys, save, update

from .usr import User

# defines

def __dir__():
    return ("cmd",)

# functions

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))
