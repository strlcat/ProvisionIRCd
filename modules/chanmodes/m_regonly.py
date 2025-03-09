"""
provides chmode +R (only registered users can join) and +M (only registered users can speak)
"""

from handle.core import Channelmode, Numeric, Hook, ChanPrivReq


def chmode_R_is_ok(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanadmin(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if client.has_permission("channel:override:mode"):
			return ChanPrivReq.ACCESSOK

		if action == '+':
			allregs = True
			for member in channel.members:
				mclient = member.client
				if not ('r' in mclient.user.modes or mclient.is_service):
					allregs = False
					break
			if not allregs:
				client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'R', '*', "All clients on channel must be registered to set mode +R.")
				return ChanPrivReq.DONTSENDERROR

		return ChanPrivReq.ACCESSOK
	return err

def reg_only_join(client, channel, key):
	if client.has_permission("channel:override:join:regonly"):
		return 0
	if channel.is_owner(client):
		return 0

	if 'R' in channel.modes and 'r' not in client.user.modes:
		return Numeric.ERR_NEEDREGGEDNICK

	return 0

def reg_only_speak(client, channel, msg, sendtype):
	if 'M' not in channel.modes:
		return Hook.ALLOW

	if channel.client_has_membermodes(client, "vhoaq") or client.has_permission("channel:override:message:regonly"):
		return Hook.ALLOW

	# joining an empty channel with, say, a bot controlling channel shall be still permitted yet speaking must be moderated by that bot.
	if ('M' in channel.modes or 'R' in channel.modes) and 'r' not in client.user.modes:
		client.sendnumeric(Numeric.ERR_CANNOTSENDTOCHAN, channel.name, "you need a registered nickname")
		return Hook.DENY

	return Hook.ALLOW

def init(module):
	Chmode_R = Channelmode()
	Chmode_R.flag = 'R'
	Chmode_R.is_ok = chmode_R_is_ok
	Chmode_R.level = 4
	Chmode_R.desc = "Only registered users may join"
	Channelmode.add(module, Chmode_R)
	Hook.add(Hook.CAN_JOIN, reg_only_join)

	Chmode_M = Channelmode()
	Chmode_M.flag = 'M'
	Chmode_M.is_ok = Channelmode.allow_halfop
	Chmode_R.level = 2
	Chmode_M.desc = "Only registered users may speak"
	Channelmode.add(module, Chmode_M)
	Hook.add(Hook.CAN_SEND_TO_CHANNEL, reg_only_speak)
