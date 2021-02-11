# This file is placed in the Public Domain

import os
import shutil
import threading
import time

from op.run import cfg
from op.dbs import find, last, list_files, last_match
from op.obj import Object, format, get, save, update
from op.hdl import Bus
from op.prs import elapsed, parse
from op.run import cfg, starttime
from op.utl import fntime, get_name

def __dir__():
    return ("flt", "thr", "upt")

def flt(event):
    try:
        event.reply(str(Bus.objs[event.prs.index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([get_name(o) for o in Bus.objs]))

def thr(event):
    psformat = "%s %s"
    result = []
    for thr in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thr).startswith("<_"):
            continue
        o = Object()
        update(o, thr)
        if get(o, "sleep", None):
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
        res.append("%s %s" % (txt, elapsed(up)))
    if res:
        event.reply(" | ".join(res))

def upt(event):
    event.reply(elapsed(time.time() - starttime))
