# OPLIB - Object Programming Library (hdl.py)
#
# This file is placed in the Public Domain.

import inspect
import importlib
import importlib.util
import os
import queue
import sys
import threading
import time

from .obj import Cfg, Default, Object, Ol, get, update
from .prs import parse
from .thr import launch
from .utl import direct, mods, spl

def __dir__():
    return ("Bus", "Command", "Event", "Handler", "cmd")

class Bus(Object):

    objs = []

    def __call__(self, *args, **kwargs):
        return Bus.objs

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        Bus.objs.append(obj)

    @staticmethod
    def announce(txt, skip=None):
        for h in Bus.objs:
            if skip is not None and isinstance(h, skip):
                continue
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def by_orig(orig):
        for o in Bus.objs:
            if repr(o) == orig:
                return o

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if repr(o) == orig:
                o.say(channel, str(txt))

class Event(Default):

    __slots__ = ("prs", "src")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.channel = ""
        self.done = threading.Event()
        self.orig = None
        self.prs = Default()
        self.result = []
        self.thrs = []
        self.type = "event"

    def direct(self, txt):
        Bus.say(self.orig, self.channel, txt)

    def parse(self):
        parse(self.prs, self.otxt or self.txt)
        args = self.prs.txt.split()
        if args:
            self.cmd = args.pop(0)
        if args:
            self.args = list(args)
            self.rest = " ".join(self.args)
            self.otype = args.pop(0)
        if args:
            self.xargs = args

    def ready(self):
        self.done.set()

    def reply(self, txt):
        self.result.append(txt)

    def show(self):
        for txt in self.result:
            self.direct(txt)

    def wait(self, timeout=1.0):
        self.done.wait(timeout)
        for thr in self.thrs:
            thr.join()

class Command(Event):

    def __init__(self, txt, **kwargs):
        super().__init__([], **kwargs)
        self.type = "cmd"
        if txt:
            self.txt = txt.rstrip()

class Handler(Object):

    threaded = False

    def __init__(self):
        super().__init__()
        self.cbs = Object()
        self.cfg = Cfg()
        self.cmds = Object()
        self.modnames = Object()
        self.names = Ol()
        self.pkgs = []
        self.queue = queue.Queue()
        self.stopped = False
        self.table = Object()

    def announce(self, txt):
        self.direct(txt)

    def clone(self, hdl):
        update(self.cmds, hdl.cmds)
        update(self.cbs, hdl.cbs)
        update(self.modnames, hdl.modnames)
        update(self.names, hdl.names)
        self.pkgs = hdl.pkgs
        self.table = hdl.table

    def cmd(self, txt):
        self.register("cmd", cmd)
        c = Command(txt)
        c.orig = repr(self)
        cmd(self, c)
        c.wait()

    def direct(self, txt):
        pass
        
    def dispatch(self, event):
        if event.type and event.type in self.cbs:
            self.cbs[event.type](self, event)

    def fromdir(self, pkgpath, name=""):
        if not pkgpath:
            return
        if not os.path.exists(pkgpath):
            return
        path = os.path.dirname(pkgpath)
        if not name:
            name = pkgpath.split(os.sep)[-1]
        sys.path.insert(0, path)
        for mn in [x[:-3] for x in os.listdir(pkgpath)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            self.load("%s.%s" % (name, mn))

    def init(self, mns, name="op"):
        thrs = []
        for mn in spl(mns):
            for name in self.pkgs:
                try:
                    spec = importlib.util.find_spec("%s.%s" % (name, mn))
                except ModuleNotFoundError:
                    continue
                if spec:
                    mod = self.load("%s.%s" % (name, mn))
                    func = getattr(mod, "init", None)
                    if func:
                        thrs.append(func(self))
        return [t for t in thrs if t]

    def intro(self, mod):
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if o.__code__.co_varnames[0] == "obj":
                    self.register(key, o)
                elif o.__code__.co_varnames[0] == "event":
                    self.cmds[key] = o
                self.modnames[key] = o.__module__
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)

    def load(self, mn):
        if mn in self.table:
            return self.table[mn]
        self.table[mn] = direct(mn)
        self.intro(self.table[mn])
        return self.table[mn]

    def handler(self):
        self.running = True
        while not self.stopped:
            e = self.queue.get()
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            e.thrs.append(launch(self.dispatch, e))

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def say(self, channel, txt):
        self.direct(txt)

    def start(self):
        launch(self.handler)

    def stop(self):
        self.stopped = True
        self.queue.put(None)

    def walk(self, pkgnames):
        for pn in spl(pkgnames):
            try:
                mod = direct(pn)
            except ModuleNotFoundError:
                continue
            self.pkgs.append(pn)
            got = False
            for name, m in inspect.getmembers(mod, inspect.ismodule):
                if pn in str(m):
                    self.load(m)
                    got = True
            if got:
                continue
            if "__file__" in dir(mod) and mod.__file__:
                p = os.path.dirname(mod.__file__)
            else:
                p = list(mod.__path__)[0]
            self.fromdir(p, pn)

    def wait(self):
        while not self.stopped:
            time.sleep(30.0)

def cmd(handler, obj):
    obj.parse()
    f = get(handler.cmds, obj.cmd, None)
    res = None
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res
