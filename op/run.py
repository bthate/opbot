# OPLIB - Object Programming Library (run.py)
#
# This file is placed in the Public Domain.

__version__ = 3

import os, sys, time

from .bsc import Basic, Test
from .obj import Cfg
from .prs import parse

cfg = Cfg()
cfg.starttime = time.time()
cfg.debug = False
cfg.verbose = False
cfg.mods = ""
cfg.opts = ""
cfg.md = ""
cfg.wd = ""

def execute(main):
    try:
        main()
    except KeyboardInterrupt:
        print("")
    except PermissionError as ex:
        print(str(ex))

def parse_cli():
    parse(cfg, " ".join(sys.argv[1:]))
    cfg.sets.wd = cfg.wd = cfg.sets.wd or cfg.wd
    assert cfg.wd
    return cfg
