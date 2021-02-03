# OP - Object Programming Library (ver.py)
#
# This file is in the Public Domain

from  .irc import __version__

def ver(event):
    event.reply("OPBOT %s" % __version__)