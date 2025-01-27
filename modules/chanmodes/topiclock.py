"""
provides chmode +T (restrict /TOPIC usage to higher operator levels)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport, ChanPrivReq

HEADER = {
	"name": "channeltlocks"
}

def topiclock_change_permitted(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanadmin(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if CHK_TYPE == Channelmode.CHK_ACCESS:
			return ChanPrivReq.ACCESSOK
		if CHK_TYPE == Channelmode.CHK_PARAM:
			if param[0] not in 'vhoaq':
				return ChanPrivReq.DONTSENDERROR
			if param[1] not in ':#':
				return ChanPrivReq.DONTSENDERROR
			if param[0] in 'q':
				return Channelmode.allow_chanowner(client, channel, action, mode, param, CHK_TYPE)
		return ChanPrivReq.ACCESSOK
	return err

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
	Chmode_T.is_ok = topiclock_change_permitted
	Chmode_T.level = 4
	Chmode_T.type = Channelmode.LISTMODE
	Chmode_T.param_help = '<vhoaq>:<nick!ident@host>'
	Chmode_T.desc = 'Restricts channel mode changes to specified operator levels'
	Channelmode.add(module, Chmode_T)
	Isupport.add("TLKLIST")
