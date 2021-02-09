# This file is placed in the Public Domain

import os, shutil

from op.obj import Object, format, save, update
from op.run import cfg
from op.prs import parse

def set(event):
    p = Object()
    parse(p, event.rest)
    update(cfg, p)
    save(cfg)
    event.reply("ok")

def sys(event):
    event.reply(format(cfg))
