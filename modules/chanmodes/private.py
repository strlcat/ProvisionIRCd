"""
channel mode +p
"""

from handle.core import Numeric, Channelmode, IRCD, ChanPrivReq

def set_cloak_name(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanop(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if 'x' in channel.modes and not client.has_permission("channel:override:mode"):
			client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'p', '*', "You cannot set both +p and +x at the same time.")
			return ChanPrivReq.DONTSENDERROR
		if action == '+':
			channel.cloakedname = IRCD.get_cloak(client, channel.name).split('.')[0]
		elif action == '-':
			channel.cloakedname = channel.name
	return err

def init(module):
	Cmode_p = Channelmode()
	Cmode_p.flag = 'p'
	Cmode_p.paramcount = 0
	Cmode_p.level = 3
	Cmode_p.is_ok = set_cloak_name
	Cmode_p.desc = "Private channel, removes details from /list and disables /knock"
	Channelmode.add(module, Cmode_p)
