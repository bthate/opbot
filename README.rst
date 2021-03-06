README
######

Welcome to OPBOT,

OPBOT is a pure python3 IRC chat bot that can run as a background daemon
for 24/7 a day presence in a IRC channel. It installs itself as a service so
you can get it restarted on reboot. You can use it to display RSS feeds, act as a
UDP to IRC gateway, program your own commands for it, have it log objects on
disk and search. 

OPBOT is placed in the Public Domain, no COPYRIGHT, no LICENSE.

INSTALL
=======

installation is through pypi:

::

 > sudo pip3 install opbot

SERVICE
=======

If you want to run the bot 24/7 you can install OPBOT as a service for
the systemd daemon. You can do this by copying the following into
the /etc/systemd/system/opbot.service file, enable it and call restart:

::

 $ sudo cp opbot.service /etc/systemd/system
 $ sudo systemctl enable opbot
 $ sudo systemctl daemon-reload
 $ sudo systemctl start opbot

default channel/server to join is #opbot on localhost.

to configure opbot use the cfg command:

::

 $ sudo opctl cfg server=<server> channel=<channel> nick=<nick>

add your userhost to the bot by introducing yourself as a user:

::

 $ sudo opctl met <userhost>

the bot should now listen to the !cmd typed.

if you don't want opbot to startup at boot, remove the service file:

::

 $ sudo rm /etc/systemd/system/opbot.service

OPCTL
=====

OPBOT has it's own CLI, the opctl program. It needs root because the opbot
program uses systemd to get it started after a reboot. You can run it on 
the shell prompt and, as default, it won't do anything.

:: 

 $ sudo opctl
 $ 

you can use opctl <cmd> to run a command directly, use the cmd command to see a list of commands:

::

 $ sudo opctl cmd
 cfg,cmd,dne,dpl,fnd,ftc,log,mbx,rem,rss,tdo,tsk,udp,upt,ver


IRC
===

configuration is done with the cfg command:

::

 $ sudo opctl cfg
 channel=#opbot nick=opbot port=6667 server=localhost

you can use setters to edit fields in a configuration:

::

 $ sudo opctl cfg server=irc.freenode.net channel=\#dunkbots nick=opbot
 ok

add you irc client's userhost to the bot:

::

 $ sudo opctl met ~botfather@jsonbot/daddy
 ok

then restart the opbot service:

::

 $ sudo systemctl restart opbot

the bot should listen to your commands now, try !cmd.

RSS
===

OPBOT provides with the use of feedparser the possibility to server rss
feeds in your channel. OPBOT runs with no dependancies and feedparser needs
to be installed to have rss feeds working:

::

 $ sudo apt install python3-feedparser

to add an url use the rss command with an url:

::

 $ sudo opctl rss https://github.com/bthate/opbot/commits/master.atom
 ok 1

run the rss command to see what urls are registered:

::

 $ sudo opctl fnd rss
 0 https://github.com/bthate/opbot/commits/master.atom

the ftc (fetch) command can be used to poll the added feeds:

::

 $ sudo opctl ftc
 fetched 20

adding rss to mods= will load the rss module and start it's poller.

::

 $ sudo bot mods=irc,rss

UDP
===

OPBOT also has the possibility to serve as a UDP to IRC relay where you
can send UDP packages to the bot and have txt displayed on the channel.

adding the udp to mods= load the udp to irc gateway

::

 $ sudo opbot mods=irc,udp

use the 'opudp' command to send text via the bot to the channel on the irc server:

::

 $ tail -f /var/log/syslog | opudp

output to the IRC channel can be done with the use python3 code to send a UDP packet 
to OPBOT, it's unencrypted txt send to the bot and display on the joined channels.

to send a udp packet to OPBOT in python3:

::

 import socket

 def toudp(host=localhost, port=5500, txt=""):
     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     sock.sendto(bytes(txt.strip(), "utf-8"), host, port)

MODULES
=======

OPBOT provides the following modules:

::

    op.clk              - clock/repeater
    op.dbs              - databases
    op.hdl              - handler
    op.itr              - introspection
    op.obj              - objects
    op.prs              - parser
    op.run              - runtime
    op.tbl              - tables
    op.thr              - threads
    op.trm              - terminal
    op.utl              - utilities

::

    opbot.cli		- cli commands
    opbot.cmd		- list of commands
    opbot.ent		- log and todo
    opbot.fnd		- locate objects
    opbot.irc		- internet relay chat
    opbot.rss		- Rich Site Syndicate
    opbot.sys		- system commands
    opbot.udp		- Uniform Datagram Protocol
    opbot.usr		- users
    opbot.ver		- version


CONTACT
=======

"contributed back to society"

| Bart Thate (bthate@dds.nl, thatebart@gmail.com)
| botfather on #dunkbots at irc.freenode.net
