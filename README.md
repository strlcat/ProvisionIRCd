## Description

A modern IRCd written in Python 3.10. Support for lower versions has officially been dropped.
<br>
Massive code overhaul, so there might still be some issues. List of found ones can be found
in TODO.md file, with "BUG:" prefixed lines. Some are outstanding ones...

This is fork from **Y4kuzi** developed by **Andrey Rys**.
The original is located at: <a href="https://github.com/Y4kuzi/ProvisionIRCd/">ProvisionIRCd</a>

## Installation

Install the required packages:
```pip3 install -r requirements.txt```

Edit <b>conf/examples/ircd.example.conf</b> and save it to <b>conf/ircd.conf</b>.<br>
When you are done editting the configuration files, you can start ProvisionIRCd by running ```python3 ircd.py```

## Features

This ircd is feature rich, as an attempt to extend and modernize an old fashioned IRC protocol.

- Full UTF-8 nickname and channel names support
- IRCv3 features
- Full TLS support
- IPv6 dualstack support [WIP separate v4 & v6 sockets]
- Full implicit CIDR support (including IPv6), including in channel bans etc.
- Extended channel and server bans, akin to UnrealIRCD ones
- Linking capabilities [THIS FORK IS NOT TESTED BUT IT SHALL WORK]
- Flexible oper permissions system
- Unique channel owner status (there can be only one, if not overriden by services)
- Configurable default channel operator status (you can even disable implicit operator status at all)
- Channel access (+A) list allowing to return ops to people who lost them, automatically or manually
- Channel mute (+B) list, allowing to mute people instead of banning them outright (although +b also mutes automatically)
- Channel modelock (+M) list, allowing to limit channel configuration without fear giving out operator access
- Channel kicklock (+K) list, allowing to limit kickban actions to restricted circle of people without fear giving out operator access to others
- Channel topiclock (+T) list, giving possibility to manage list of people who can set topics
- Minimum _embedded_ services: CHANFIX and OPME (not working as EFnet ones, these are _very simpler_ to understand),
  which permits running server completely on its own, without services required, which may allow running IRCD without
  any external services at all
- Services-less friendly, a super operator bot such as scripted eggdrop instance can work as a service [WIP]

## Services

Barely if just you want to run this IRCd without bothering with services:

Comment out file with service aliases, such as, **aliases.conf**. Because thise are responsible for proxying messages between you
and services, a failure do do so will usually emit something frustrtating like ":Services are currently down. Please try again later.",
giving you (false) impression that they shall be here and they will be soon returning.

This IRCd provides two self-healing services for people who lost their channel operator roles:

1. **/CHANFIX** is the first and very precise about checking, and restoring operator status.
   It acts _immediately_, so you have not to wait, unless the real HW behind server is doing something very important.

2. **/OPME** works if you have channel access list entry, but it is limited to highest +a channel operator role.

## Issue

If you find a bug or have a feature request, you can <a href="https://github.com/strlcat/ProvisionIRCd/issues/new">submit an issue</a>
<br> to this fork
or you can contact me on IRC rys @ irc.strl.cat when I'm not afk.

This work is just an expression of ideas. No functionality herein implemented is guaranteed to be bug free.
Certainly, multiple server linking was not tested at all. Submit a bug report if you think something is broken.

## Rys fork notes

This is a fork of ProvisionIRCd by Y4kuzi hosted at https://strlcat.eu/rys/ProvisionIRCd/

A live server is running at <b>irc.strl.cat</b> ports 6667 (plain) and 6697 (TLS), with Anope 2.0+

No IRCOp status is currently provided there yet to test, but you might join and request one from rys or strlcat. I don't bite.

Default channel modes are +nt and default channel operator status given to you is +qo (owner).
Of course if channel is registered to someone else, services will remove operator from you.
Anope was modified to require channel owner status from you when registering one. It is oneline
modification which is very easy to locate, so to find out how it was implemented will be left
as a homework exercise for a reader. (SPOILER: for Anope 2.0x, look around inside
modules/commands/cs\_register.cpp HasUserStatus OP -> OWNER, got it?)

No HostServ or MemoServ are enabled for simplicity. You can assign ChanServ to a channel.

From there, you can proceed with usual NickServ/ChanServ registration. No verification required,
although also no password recovery possible too, so it is RECOMMENDED to connect via TLS with
user generated certificate, register nickname and then add that certificate fingerprint to
NickServ so it will always auto-authenticate you next time you will connect to server.

There will be a minimum nickname length restriction of 3 characters, to prevent aliases abuse.

If server is offline for some reason, just wait a week or two - instance sits on a RISC-V dev machine at my home in Prague.
It means that I am traveling during downtime, and power at my home is completely shutdown to prevent accidents.
This notice will be removed once I will migrate it to my VPS, but right now I am too lazy to do that.
