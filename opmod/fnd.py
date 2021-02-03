# OP - Object Programming Library (fnd.py)
#
#

import op
import op.cfg

from op.dbs import find, list_files
from op.prs import elapsed
from op.utl import fntime, get_names

def fnd(event):
    if not event.args:
        fls = list_files(op.cfg.wd)
        if fls:
            event.reply(" | ".join([x.split(".")[-1].lower() for x in fls]))
        return
    nr = -1
    name = event.args[0]
    names = get_names("op")
    types = op.get(names, name, [name])
    modnames = get_names("mod")
    types2 = op.get(modnames, name, [name])
    for otype in types + types2:
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), op.format(o, event.xargs or op.keys(o), skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
