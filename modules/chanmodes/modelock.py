"""
provides chmode +M (restrict channel modes to higher operator levels)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport, ChanPrivReq

HEADER = {
	"name": "channelmlocks"
}

def modelock_change_permitted(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanowner(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if CHK_TYPE == Channelmode.CHK_ACCESS:
			return ChanPrivReq.ACCESSOK
		if CHK_TYPE == Channelmode.CHK_PARAM:
			if param[0] not in 'hoaq':
				return ChanPrivReq.DONTSENDERROR
			if param[1] not in ':#':
				return ChanPrivReq.DONTSENDERROR
		return ChanPrivReq.ACCESSOK
	return err

def display_mlocklist(client, channel, mode):
	if mode == "M":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:mlocklist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ANYLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFANYLIST, channel.name, "Modelock")
		return 1

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_mlocklist)
	Chmode_M = Channelmode()
	Chmode_M.flag = 'M'
	Chmode_M.sjoin_prefix = '?'
	Chmode_M.paramcount = 1
	Chmode_M.unset_with_param = 1
	Chmode_M.is_ok = modelock_change_permitted
	Chmode_M.level = 5
	Chmode_M.type = Channelmode.LISTMODE
	Chmode_M.param_help = '<hoaq>:<nick!ident@host>'
	Chmode_M.desc = 'Restricts channel mode changes to specified operator levels'
	Channelmode.add(module, Chmode_M)
	Isupport.add("MLKLIST")
