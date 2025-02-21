"""
provides chmode +R (only registered users can join) and +M (only registered users can speak)
"""

from handle.core import Channelmode, Numeric, Hook

def reg_only_join(client, channel, key):
	if client.has_permission("channel:override:join:regonly"):
		return 0

	# The chanfix check is not applicable here because if channel
	# has mode +r set, the chanfix channel owner info is erased.
	if 'R' in channel.modes and 'r' in channel.modes and 'r' not in client.user.modes:
		return Numeric.ERR_NEEDREGGEDNICK

	return 0

def reg_only_speak(client, channel, msg, sendtype):
	if 'M' not in channel.modes:
		return Hook.ALLOW

	if channel.client_has_membermodes(client, "vhoaq") or client.has_permission("channel:override:message:regonly"):
		return Hook.ALLOW

	# Omit +r channel mode check: joining an empty channel with, say, a bot
	# controlling channel shall be still permitted yet speaking must be moderated by that bot.
	if 'M' in channel.modes and 'r' not in client.user.modes:
		client.sendnumeric(Numeric.ERR_CANNOTSENDTOCHAN, channel.name, "you need a registered nickname")
		return Hook.DENY

	return Hook.ALLOW

def init(module):
	Hook.add(Hook.CAN_JOIN, reg_only_join)
	Chmode_R = Channelmode()
	Chmode_R.flag = 'R'
	Chmode_R.is_ok = Channelmode.allow_chanadmin
	Chmode_R.desc = "Only registered users may join"
	Channelmode.add(module, Chmode_R)
	Chmode_M = Channelmode()
	Chmode_M.flag = 'M'
	Chmode_M.is_ok = Channelmode.allow_halfop
	Chmode_M.desc = "Only registered users may speak"
	Channelmode.add(module, Chmode_M)
	Hook.add(Hook.CAN_SEND_TO_CHANNEL, reg_only_speak)
