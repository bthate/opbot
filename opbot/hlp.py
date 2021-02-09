# This file is placed in the Public Domain

"""OPBOT(1)			   User Commands 			 OPBOT(1)

NAME
        OPBOT - operbot.

SYNOPSIS
        opbot <cmd> [mods=mod1,mod2] [-d] [-h] [-s] [-v]

DESCRIPTION
        OPBOT is a pure python3 IRC chat bot that can run as a background daemon
        for 24/7 a day presence in a IRC channel. It installs itself as a service so
        you can get it restarted on reboot. You can use it to display RSS feeds, act as a
        UDP to IRC gateway, program your own commands for it, have it log objects on
        disk and search. 

        OPBOT is placed in the Public Domain, no COPYRIGHT, no LICENSE.

EXAMPLES
        1) opbot cfg server=<server> channel=<channel> nick=<nick>
        2) opbot met <userhost>
        3) opbot rss <url>
        4) opbot ftc
        5) opbot cmd
        6) opbot mods=irc

OPTIONS
        -c		start console
        -l		load config
        -r		use /var/lib/opbot/
        -s              save config
        -h              print this message
        -v              be verbose
        -w		wait 
"""
