"""
provides chmode +b (ban list)
"""

from handle.core import Numeric, Channelmode, Hook, ChanPrivReq
from handle.functions import get_higher_opers_than

HEADER = {
	"name": "channelbans"
}

def ok_to_ban(client, channel, action, mode, param, CHK_TYPE):
	if len(channel.List['K']) > 0:
		opmode = channel.has_access(client, 'K', "hoaq", -1)
		if opmode:
			if not channel.client_has_membermodes(client, get_higher_opers_than(opmode)):
				return ChanPrivReq.NOTOWNER
		else:
			return ChanPrivReq.NOTOWNER
	return Channelmode.allow_halfop(client, channel, action, mode, param, CHK_TYPE)

def display_banlist(client, channel, mode):
	if mode == "b":
		if channel.client_has_membermodes(client, "hoaq") or client.has_permission("channel:see:banlist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_BANLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFBANLIST, channel.name)
		return 1

def ban_can_join(client, channel, key):
	if (channel.is_banned(client) and not channel.is_exempt(client)) and not client.has_permission("override:channel:join:ban"):
		return Numeric.ERR_BANNEDFROMCHAN
	return 0

def msg_banned(client, channel, message, sendtype):
	if (channel.is_banned(client) and not channel.client_has_membermodes(client, "hoaq") and not channel.is_exempt(client)) and not client.has_permission("override:channel:message:ban"):
		client.sendnumeric(Numeric.ERR_CANNOTSENDTOCHAN, channel.name, "Cannot send to channel (+b)")
		return Hook.DENY
	return Hook.ALLOW

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_banlist)
	Hook.add(Hook.CAN_JOIN, ban_can_join)
	Hook.add(Hook.CAN_SEND_TO_CHANNEL, msg_banned)
	Chmode_b = Channelmode()
	Chmode_b.flag = 'b'
	Chmode_b.sjoin_prefix = '&'
	Chmode_b.paramcount = 1
	Chmode_b.unset_with_param = 1
	Chmode_b.is_ok = ok_to_ban
	Chmode_b.level = 2
	Chmode_b.type = Channelmode.LISTMODE
	Chmode_b.param_help = '<nick!ident@host>'
	Chmode_b.desc = 'Bans the given hostmask from joining the channel'
	Channelmode.add(module, Chmode_b)
