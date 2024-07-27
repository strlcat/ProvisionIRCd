## Description

A modern IRCd written in Python 3.10. Support for lower versions has officially been dropped.
<br>
Massive code overhaul, so there might still be some issues. List of found ones can be found
in TODO.md file, with "BUG:" prefixed lines. Some are outstanding ones...

## Installation

Install the required packages:
```pip3 install -r requirements.txt```

Edit <b>conf/examples/ircd.example.conf</b> and save it to <b>conf/ircd.conf</b>.<br>
When you are done editting the configuration files, you can start ProvisionIRCd by running ```python3 ircd.py```

## Features

- Very modular, all modules can be reloaded on the fly (not always recommended)
- IRCv3 features
- Full TLS support
- IPv6 dualstack support
- Full implicit CIDR support (including IPv6), including in channel bans etc.
- Extended channel and server bans
- Linking capabilities
- Flexible oper permissions system
- Unique channel owner status (there can be only one)
- Configurable default channel operator status (you can even disable implicit operator status at all)

## Services

To use Anope with ProvisionIRCd, load the <b>unreal4</b> protocol module in Anope services.conf.
It is well tested and fully compatible, causing no any problems with linking.
Note that only C++ Anope 2.0+ is known to work there because old pure C Anope speaks too old protocol.

The server itself is quite capable of running on its own without services, provided there will be
a network wide IRC operator who could manage user and channel modes. (which is possible thanks to ircop permissions)
For example, a highly scripted eggdrop bot instance functioning like well-known CHANFIX.

## Issue

If you find a bug or have a feature request, you can <a href="https://github.com/Y4kuzi/ProvisionIRCd/issues/new">submit an issue</a>
<br>
or you can contact me on IRC @ irc.provisionweb.org when I'm not afk.

## Rys fork notes

This is a fork of ProvisionIRCd by Y4kuzi hosted at https://strlcat.eu/rys/ProvisionIRCd/

A live server is running at <b>irc.strl.cat</b> ports 6667 (plain) and 6697 (TLS), with Anope 2.0+

No oper status is currently provided there yet, but you might join and request one from rys.

Default channel modes are +nt and default oper status given to you is +qo (owner).
Of course if channel is registered to someone else, services will remove operator from you.

No HostServ or MemoServ are enabled for simplicity. You can assign ChanServ to a channel.

From there, you can proceed with usual NickServ/ChanServ registration. No verification required,
although also no password recovery possible too, so it is RECOMMENDED to connect via TLS with
user generated certificate, register nickname and then add that certificate fingerprint to
NickServ so it will always auto-authenticate you next time you will connect to server.
