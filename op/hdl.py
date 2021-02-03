# OP - Object Programming Library (hdl.py)
#
# This file is placed in the Public Domain.

import inspect
import importlib
import importlib.util
import op
import os
import queue
import sys
import threading
import time

from op.dbs import last
from op.prs import parse
from op.thr import launch
from op.utl import direct, spl

def __dir__():
    return ("Bus", "Command", "Event", "Handler", "cmd")

class Bus(op.Object):

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

class Event(op.Default):

    __slots__ = ("prs", "src")

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.channel = ""
        self.done = threading.Event()
        self.orig = None
        self.prs = op.Default()
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

class Handler(op.Object):

    threaded = False

    def __init__(self):
        super().__init__()
        self.cbs = op.Object()
        self.cfg = op.Cfg()
        self.cmds = op.Object()
        self.modnames = op.Object()
        self.names = op.Ol()
        self.queue = queue.Queue()
        self.stopped = False
        Bus.add(self)

    def __str__(self):
        return str(self.cfg)

    def clone(self, hdl):
        op.update(self.cmds, hdl.cmds)
        op.update(self.cbs, hdl.cbs)
        op.update(self.modnames, hdl.modnames)
        op.update(self.names, hdl.names)

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

    def fromdir(self, pkgpath, name="op"):
        if not pkgpath:
            return
        if not os.path.exists(pkgpath):
            return
        path = os.path.dirname(pkgpath)
        sys.path.insert(0, path)
        for mn in [x[:-3] for x in os.listdir(pkgpath)
                   if x and x.endswith(".py")
                   and not x.startswith("__")
                   and not x == "setup.py"]:
            mnn = "%s.%s" % (name, mn)
            try:
                m = sys.modules[mnn]
            except:
                m = direct(mnn)
            self.intro(m)

    def init(self, mns, name="op"):
        thrs = []
        for mn in spl(mns):
            try:
                spec = importlib.util.find_spec("%s.%s" % (name, mn))
            except ModuleNotFoundError:
                continue
            if spec:
                mod = self.load("%s.%s" % (name, mn))
                self.intro(mod)
                func = getattr(mod, "init", None)
                if func:
                    thrs.append(func(self))
        return [t for t in thrs if t]

    def intro(self, mod):
        if op.cfg.debug:
            print("load %s" % mod.__name__)
        for key, o in inspect.getmembers(mod, inspect.isfunction):
            if o.__code__.co_argcount == 1:
                if o.__code__.co_varnames[0] == "obj":
                    self.register(key, o)
                elif o.__code__.co_varnames[0] == "event":
                    self.cmds[key] = o
                self.modnames[key] = o.__module__
        for _key, o in inspect.getmembers(mod, inspect.isclass):
            if issubclass(o, op.Object):
                t = "%s.%s" % (o.__module__, o.__name__)
                self.names.append(o.__name__.lower(), t)

    def load(self, mn):
        if mn in sys.modules:
            mod = sys.modules[mn]
        else:
            mod = direct(mn)
        self.intro(mod)
        return mod

    def handler(self, once=False):
        self.running = True
        while not self.stopped:
            try:
                e = self.queue.get(True, 1.0)
            except queue.Empty:
                if once:
                    break
                continue
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            e.thrs.append(launch(self.dispatch, e))
            if once:
                break

    def put(self, e):
        self.queue.put_nowait(e)

    def register(self, name, callback):
        self.cbs[name] = callback

    def hup(self):
        last(self.cfg)

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
            got = False
            for name, m in inspect.getmembers(mod, inspect.ismodule):
                if pn in str(m):
                    self.intro(m)
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
            time.sleep(0.5)

def cmd(handler, obj):
    obj.parse()
    f = op.get(handler.cmds, obj.cmd, None)
    res = None
    if f:
        res = f(obj)
        obj.show()
    obj.ready()
    return res
