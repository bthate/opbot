# This file is placed in the Public Domain.

import sys, time

from .obj import Cfg
from .prs import parse

cfg = Cfg()
cfg.debug = False
cfg.verbose = False
cfg.mods = ""
cfg.opts = ""
cfg.md = ""
cfg.wd = ""

starttime = time.time()

def execute(main):
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))

def parse_cli():
    parse(cfg, " ".join(sys.argv[1:]))
    if cfg.sets:
        cfg.changed = True
    cfg.sets.wd = cfg.wd = cfg.sets.wd or cfg.wd
    cfg.mods = cfg.sets.mods
    return cfg
