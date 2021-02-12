# This file is placed in the Public Domain.

import atexit, sys, termios

from op.hdl import Bus, Command, Handler, cmd
from op.thr import launch

def __dir__():
    return ("CLI", "Console", "init", "console")

resume = {}

def init(h):
    c = Console()
    c.clone(h)
    c.start()
    return c

class Console(Handler):

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)
        Bus.add(self)

    def direct(self, txt):
        print(txt)

    def input(self):
        while 1:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)
            e.wait()

    def poll(self):
        return Command(input("> "))

    def start(self):
        super().start()
        launch(self.input)

class CLI(Handler):

    def __init__(self):
        super().__init__()
        self.register("cmd", cmd)

    def direct(self, txt):
        print(txt)
