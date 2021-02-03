# OP - Object Programming Library (cmd.py)
#
# This file is placed in the Public Domain.

import op
import op.hdl

def __dir__():
    return ("cmd",)

def cmd(event):
    bot = op.hdl.Bus.by_orig(event.orig)
    if bot:
        c = sorted(op.keys(bot.cmds))
        if c:
            event.reply(",".join(c))
