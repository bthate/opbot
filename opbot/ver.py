# OPBOT - pure python3 IRC bot (bin/clean)
#
# This file is placed in the Public Domain.

"version"

# defines

__txt__ = "OTP-CR-117/19 otp.informationdesk@icc-cpi.int http://pypi.org/project/genocide !"
__version__ = 3

# commands

def ver(event):
    event.reply("OPBOT %s - pure python3 IRC bot" % __version__)
