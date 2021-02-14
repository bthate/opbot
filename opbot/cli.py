# This file is placed in the Public Domain.

import os, shutil

from op.dbs import last
from op.obj import format, save, update
from op.prs import parse

def cpy(event):
    if not os.path.exists(cfg.md):
        os.mkdir(cfg.md)
    fns = []
    p = os.path.join(os.getcwd(), "mod")
    nr = 0
    for fn in os.listdir(p):
        if not fn.endswith("py"):
            continue
        fns.append(fn)
    for fn in fns:
        fnn = os.path.join(cfg.md, fn)
        shutil.copy2("mod/%s" % fn, fnn)
        nr += 1
    event.reply("%s copied to %s" % (nr, p))

def set(event):
    if not event.otxt:
        event.reply(format(cfg))
        return
    last(cfg)
    parse(p, event.rest)
    update(cfg, p)
    save(cfg)
    event.reply("ok")
