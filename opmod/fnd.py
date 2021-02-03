# OPMOD - Object Programming Modules (fnd.py)
#
# This file is in the Public Domain.
 
from op.obj import Object, format, get, keys
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
    types = get(names, name, [name])
    modnames = get_names("opmod")
    types2 = get(modnames, name, [name])
    for otype in types + types2:
        for fn, o in find(otype, event.prs.gets, event.prs.index, event.prs.timed):
            nr += 1
            txt = "%s %s" % (str(nr), format(o, event.xargs or keys(o), skip=event.prs.skip))
            if "t" in event.prs.opts:
                txt = txt + " %s" % (elapsed(time.time() - fntime(fn)))
            event.reply(txt)
