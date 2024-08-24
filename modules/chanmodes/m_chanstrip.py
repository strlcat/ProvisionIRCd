"""
provides chmode +W (strip colors, bold, underline from messages)
"""

from handle.core import IRCD, Channelmode, Hook

def stripmsg_W(client, channel, msg):
	if 'W' in channel.modes:
		for idx, entry in enumerate(msg):
			msg[idx] = IRCD.strip_format(entry)

def init(module):
	Hook.add(Hook.PRE_LOCAL_CHANMSG, stripmsg_W)
	Hook.add(Hook.PRE_LOCAL_CHANNOTICE, stripmsg_W)
	Chmode_W = Channelmode()
	Chmode_W.flag = 'W'
	Chmode_W.is_ok = Channelmode.allow_halfop
	Chmode_W.desc = "Strip colors and other formatting from channel messages"
	Channelmode.add(module, Chmode_W)
