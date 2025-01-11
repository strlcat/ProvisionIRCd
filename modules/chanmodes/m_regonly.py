"""
provides chmode +R (only registered users can join)
"""

from handle.core import Channelmode, Numeric, Hook

def reg_only_join(client, channel, key):
	# The chanfix check is not applicable here because if channel
	# has mode +r set, the chanfix channel owner info is erased.
	if 'R' in channel.modes and 'r' in channel.modes and 'r' not in client.user.modes:
		return Numeric.ERR_NEEDREGGEDNICK
	return 0

def init(module):
	Hook.add(Hook.CAN_JOIN, reg_only_join)
	Chmode_R = Channelmode()
	Chmode_R.flag = 'R'
	Chmode_R.is_ok = Channelmode.allow_chanadmin
	Chmode_R.desc = "Only registered users may join"
	Channelmode.add(module, Chmode_R)
