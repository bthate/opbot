# OP - Object Programming Library (ver.py)
#
# This file is in the Public Domain

import op

def ver(event):
    event.reply("OPLIB %s" % op.__version__)