# OP - Object Programming (dbg.py)
#
# this file is placed in the public domain

"commands (cmd)"

# imports

import op
import op.cfg
import threading
import time

from op.dbs import find, last, list_files, last_match
from op.hdl import Bus
from op.prs import elapsed
from op.utl import fntime

# defines

starttime = time.time()

def __dir__():
    return ("flt", "thr")

# commands

def flt(event):
    "list of bots"
    try:
        event.reply(str(Bus.objs[event.prs.index]))
        return
    except (TypeError, IndexError):
        pass
    event.reply(" | ".join([op.get_name(o) for o in Bus.objs]))

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
            up = int(time.time() - op.cfg.starttime)
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
    return elapsed(time.time - op.cfg.starttime)