"""
provides chmode +B (mute list)
"""

from handle.core import Numeric, Channelmode, Hook, Isupport

HEADER = {
	"name": "channelmutes"
}


def display_mutelist(client, channel, mode):
	if mode == "B":
		if channel.client_has_membermodes(client, "hoaq") or client.has_permission("channel:see:mutelist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_BANLIST, channel.name, entry.mask, entry.set_By, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFBANLIST, channel.name)
		return 1

def msg_muted(client, channel, message, sendtype):
	if (channel.is_muted(client) and not channel.client_has_membermodes(client, "hoaq") and not channel.is_exempt(client)) and not client.has_permission("override:channel:message:mute"):
		client.sendnumeric(Numeric.ERR_CANNOTSENDTOCHAN, channel.name, "Cannot send to channel (+B)")
		return Hook.DENY
	return Hook.ALLOW

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_mutelist)
	Hook.add(Hook.CAN_SEND_TO_CHANNEL, msg_muted)
	Chmode_B = Channelmode()
	Chmode_B.flag = 'B'
	Chmode_B.sjoin_prefix = '!'
	Chmode_B.paramcount = 1
	Chmode_B.unset_with_param = 1
	Chmode_B.is_ok = Channelmode.allow_halfop
	Chmode_B.level = 2
	Chmode_B.type = Channelmode.LISTMODE
	Chmode_B.param_help = '<nick!ident@host>'
	Chmode_B.desc = 'Mutes the given hostmask (like +m, but individual)'
	Channelmode.add(module, Chmode_B)
	Isupport.add("MUTELIST")
