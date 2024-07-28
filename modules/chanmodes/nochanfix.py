"""
channel mode +F
Disable chanfix service on channel.
"""

from handle.core import IRCD, Channelmode

def chmode_F_ok(client, channel, action, mode, param, CHK_TYPE):
    if not IRCD.get_setting("chanfix"):
        return 0
    if Channelmode.allow_chanadmin(client, channel, action, *[]):
        if action == '+':
            channel.founder = ''
        elif action == '-':
            channel.founder = IRCD.channel_founder_fingerprint(client)
        return 1
    return 0

def init(module):
    Cmode_F = Channelmode()
    Cmode_F.flag = 'F'
    Cmode_F.is_ok = chmode_F_ok
    Cmode_F.level = 4
    Cmode_F.desc = "Disable chanfix service on channel"
    Channelmode.add(module, Cmode_F)
