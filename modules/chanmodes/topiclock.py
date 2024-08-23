"""
provides chmode +T (restrict /TOPIC usage to higher operator levels)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport

HEADER = {
	"name": "channeltlocks"
}

def display_tlocklist(client, channel, mode):
	if mode == "T":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:tlocklist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ANYLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFANYLIST, channel.name, "Topiclock")
		return 1

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_tlocklist)
	Chmode_T = Channelmode()
	Chmode_T.flag = 'T'
	Chmode_T.sjoin_prefix = ';'
	Chmode_T.paramcount = 1
	Chmode_T.unset_with_param = 1
	Chmode_T.is_ok = Channelmode.allow_chanowner
	Chmode_T.level = 5
	Chmode_T.type = Channelmode.LISTMODE
	Chmode_T.param_help = '<vhoaq>#<nick!ident@host>'
	Chmode_T.desc = 'Restricts channel mode changes to specified operator levels'
	Channelmode.add(module, Chmode_T)
	Isupport.add("TLKLIST")
