"""
channel mode +p
"""

from handle.core import Channelmode, IRCD, ChanPrivReq

def set_cloak_name(client, channel, action, mode, param, CHK_TYPE):
	if not Channelmode.allow_chanop(client, channel, action, mode, param, CHK_TYPE):
		return ChanPrivReq.NOTOPER
	if action == '+':
		channel.cloakedname = IRCD.get_cloak(client, channel.name).split('.')[0]
	elif action == '-':
		channel.cloakedname = "*"
	return ChanPrivReq.ACCESSOK

def init(module):
	Cmode_p = Channelmode()
	Cmode_p.flag = 'p'
	Cmode_p.paramcount = 0
	Cmode_p.is_ok = set_cloak_name
	Cmode_p.desc = "Private channel, removes details from /list and disables /knock"
	Channelmode.add(module, Cmode_p)
