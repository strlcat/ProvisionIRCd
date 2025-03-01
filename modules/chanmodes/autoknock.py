"""
channel mode +x (automatically knock to channel)
"""

from handle.core import Numeric, Channelmode, ChanPrivReq

def chmode_x_is_ok(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanop(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if 'p' in channel.modes and not client.has_permission("channel:override:mode"):
			client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'x', '*', "You cannot set both +x and +p at the same time.")
			return ChanPrivReq.DONTSENDERROR
	return err

def init(module):
	Cmode_x = Channelmode()
	Cmode_x.flag = 'x'
	Cmode_x.sets_modes = 'i'
	Cmode_x.level = 3
	Cmode_x.paramcount = 0
	Cmode_x.is_ok = chmode_x_is_ok
	Cmode_x.desc = "Automatically /knock when attempting to join invite only channel"
	Channelmode.add(module, Cmode_x)
