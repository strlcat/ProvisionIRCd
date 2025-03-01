"""
channel mode +Z (requires TLS to join the channel)
"""

from handle.core import Numeric, Channelmode, Hook, ChanPrivReq

def chmode_Z_is_ok(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanadmin(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if client.has_permission("channel:override:mode"):
			return ChanPrivReq.ACCESSOK

		if action == '+':
			secure = True
			for member in channel.members:
				mclient = member.client
				if not ('z' in mclient.user.modes or 'S' in mclient.user.modes):
					secure = False
					break
			if not secure:
				client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'Z', '*', "All clients on channel must be connected securely to set mode +Z.")
				return ChanPrivReq.DONTSENDERROR

		return ChanPrivReq.ACCESSOK
	return err

def chmode_Z_only_join(client, channel, key):
	if client.has_permission("channel:override:join:secureonly"):
		return 0
	if channel.is_owner(client):
		return 0
	if 'Z' in channel.modes and 'z' not in client.user.modes:
		return Numeric.ERR_SECUREONLY
	return 0

def init(module):
	Cmode_Z = Channelmode()
	Cmode_Z.flag = 'Z'
	Cmode_Z.is_ok = chmode_Z_is_ok
	Cmode_Z.level = 4
	Cmode_Z.desc = "Requires a TLS connection to join the channel"
	Channelmode.add(module, Cmode_Z)
	Hook.add(Hook.CAN_JOIN, chmode_Z_only_join)
