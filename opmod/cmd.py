# This file is placed in the Public Domain.

import threading
import time

from op.dbs import find, last, list_files, last_match
from op.obj import Object, format, get, keys, save, update
from op.hdl import Bus
from op.prs import elapsed, parse
from op.run import cfg, starttime
from op.utl import fntime, get_name

def __dir__():
    return ("cmd", )

def cmd(event):
    bot = Bus.by_orig(event.orig)
    if bot:
        c = sorted(keys(bot.cmds))
        if c:
            event.reply(",".join(c))
