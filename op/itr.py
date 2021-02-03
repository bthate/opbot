# OP - Object Programming Library (itr.py)
#
# This file is placed in the Public Domain.

import op
import importlib
import inspect
import pkgutil

from op.utl import direct

def find_cmds(mod):
    cmds = op.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                cmds[key] = o
    return cmds

def find_funcs(mod):
    funcs = op.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                funcs[key] = "%s.%s" % (o.__module__, o.__name__)
    return funcs

def find_mods(mod):
    mods = op.Object()
    for key, o in inspect.getmembers(mod, inspect.isfunction):
        if "event" in o.__code__.co_varnames:
            if o.__code__.co_argcount == 1:
                mods[key] = o.__module__
    return mods

def find_classes(mod):
    nms = op.Ol()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, op.Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            nms.append(o.__name__, t)
    return nms

def find_class(mod):
    mds = op.Ol()
    for key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, op.Object):
            mds.append(o.__name__, o.__module__)
    return mds

def find_names(mod):
    tps = op.Ol()
    for _key, o in inspect.getmembers(mod, inspect.isclass):
        if issubclass(o, op.Object):
            t = "%s.%s" % (o.__module__, o.__name__)
            tps.append(o.__name__.lower(), t)
    return tps
