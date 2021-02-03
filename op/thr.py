# OP - Object Programming Library (thr.py)
#
# This file is placed in the Public Domain

import op
import queue
import threading

from op.utl import get_exception

class Thr(threading.Thread):

    def __init__(self, func, *args, thrname="", daemon=True):
        super().__init__(None, self.run, thrname, (), {}, daemon=daemon)
        self._name = thrname or op.get_name(func)
        self._result = None
        self._queue = queue.Queue()
        self._queue.put_nowait((func, args))
        self.sleep = 0
        self.state = op.Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=1.0):
        ""
        super().join(timeout)
        return self._result

    def run(self):
        ""
        try:
            func, args = self._queue.get_nowait()
        except queue.Empty:
            return
        target = None
        if args:
            try:
                target = op.Default(vars(args[0]))
                self._name = (target and target.txt and target.txt.split()[0]) or self._name
            except TypeError:
                pass
        self.setName(self._name)
        if op.cfg.verbose:
             print("launch %s(%s)" % (self._name, ",".join([str(x) for x in args if x])))
        try:
            self._result = func(*args)
        except Exception as ex:
            if op.cfg.verbose:
                print(get_exception())
        self._queue.task_done()

    def wait(self, timeout=1.0):
        super().join(timeout)
        return self._result

def launch(func, *args, **kwargs):
    name = kwargs.get("name", op.get_name(func))
    t = Thr(func, *args, thrname=name, daemon=True)
    t.start()
    return t
