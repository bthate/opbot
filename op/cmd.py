# OPLIB - Object Programming Library (cmd.py)
#
# This file is placed in the Public Domain.

from .obj import keys
from .hdl import Bus

def __dir__():
    return ("cmd",)

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))
