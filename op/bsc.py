# OPLIB - Object Programming Library (bsc.py)
#
# This file is placed into the Public Domain.

from .hdl import Bus, Handler, cmd

class Core(Handler):

     def __init__(self):
         super().__init__()
         self.register("cmd", cmd)
         self.load("op.cmd")
         Bus.add(self)

class Basic(Core):
         
     def direct(self, txt):
         print(txt)
         
class Test(Core):

     def direct(self, txt):
         from .run import cfg
         if cfg.verbose:
             print(txt)