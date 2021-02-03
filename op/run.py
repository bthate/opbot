# OPLIB - Object Programming Library (run.py)
#
# This file is placed in the Public Domain.

__version__ = 3

import time

from .obj import Cfg

cfg = Cfg()
cfg.starttime = time.time()
cfg.debug = False
cfg.verbose = False
cfg.md = ""
cfg.wd = ""
