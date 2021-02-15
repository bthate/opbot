.. _manpage:

MANPAGE
=======

NAME
        OPBOT - pure python3 IRC bot.

SYNOPSIS
        1) opbot <cmd> [mods=mod1,mod2] [-c] [-h] -[l] [-r] [-v] [-w]
        2) opctl <cmd> 
        3) op <cmd>
        
DESCRIPTION
        OPBOT is a pure python3 IRC chat bot that can run as a background daemon
        for 24/7 a day presence in a IRC channel. You can use it to display RSS
        feeds, relay udp packet data to IRC channel, program your own commands
        for it and have it log objects to disk for persistence. 

        If you want to run the bot 24/7 you can install OPBOT as a service for
        the systemd daemon. You can do this by copying the following into
        the /etc/systemd/system/opbot.service file, enable it and call restart:

        ::

        $ sudo cp opbot.service /etc/systemd/system
        $ sudo systemctl enable opbot
        $ sudo systemctl daemon-reload
        $ sudo systemctl start opbot

        default channel/server to join is #opbot on localhost.

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
        -v              be verbose
        -w		wait 
