# This file is placed in the Public Domain.

import sys, time

from .obj import Cfg, save, update
from .prs import parse
from .trm import termsave, termreset

cfg = Cfg()

starttime = time.time()

def parse_cli():
    c = Cfg()
    parse(cfg, " ".join(sys.argv[1:]))
    if cfg.sets:
        cfg.changed = True
    cfg.wd = cfg.sets.wd or cfg.wd
    cfg.mods = cfg.sets.mods or cfg.mods
    return cfg
