"""
provides chmode +Q (restrict usage of /KICK to upper level operators)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport

HEADER = {
	"name": "channelklocks"
}

def display_kicklocklist(client, channel, mode):
	if mode == "Q":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:kicklocklist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ANYLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFANYLIST, channel.name, "Kicklock")
		return 1

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_kicklocklist)
	Chmode_Q = Channelmode()
	Chmode_Q.flag = 'Q'
	Chmode_Q.sjoin_prefix = '_'
	Chmode_Q.paramcount = 1
	Chmode_Q.unset_with_param = 1
	Chmode_Q.is_ok = Channelmode.allow_chanowner
	Chmode_Q.level = 5
	Chmode_Q.type = Channelmode.LISTMODE
	Chmode_Q.param_help = '<hoaq>:<nick!ident@host>'
	Chmode_Q.desc = 'Restricts /KICK to specified operator levels'
	Channelmode.add(module, Chmode_Q)
	Isupport.add("KIKLLIST")
