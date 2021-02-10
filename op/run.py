# This file is placed in the Public Domain.

import sys, time

from .obj import Cfg, save
from .prs import parse
from .trm import termsave, termreset

cfg = Cfg()

starttime = time.time()

def console(main):
    termsave()
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))
    finally:
        termreset()

def execute(main):
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))

def parse_cli(use_last=False):
    from .dbs import last
    if use_last:
       last(cfg)
    c = Cfg()
    parse(c, " ".join(sys.argv[1:]))
    if c.sets:
        cfg.changed = True
    cfg.sets.wd = cfg.wd = c.sets.wd or cfg.wd
    cfg.mods = c.sets.mods or cfg.mods
    if cfg.changed and use_last:
        save(cfg)
    return cfg
