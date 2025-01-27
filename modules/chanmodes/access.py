"""
provides chmode +A (access/autoop list)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport, ChanPrivReq

HEADER = {
	"name": "channelaccess"
}

def acclist_change_permitted(client, channel, action, mode, param, CHK_TYPE):
	err = Channelmode.allow_chanadmin(client, channel, action, mode, param, CHK_TYPE)
	if err == ChanPrivReq.ACCESSOK:
		if CHK_TYPE == Channelmode.CHK_ACCESS:
			return ChanPrivReq.ACCESSOK
		if CHK_TYPE == Channelmode.CHK_PARAM:
			if param[0] not in 'vhoa':
				return ChanPrivReq.DONTSENDERROR
			if param[1] not in ':#':
				return ChanPrivReq.DONTSENDERROR
			if param[0] in 'a':
				return Channelmode.allow_chanowner(client, channel, action, mode, param, CHK_TYPE)
		return ChanPrivReq.ACCESSOK
	return err

def display_acclist(client, channel, mode):
	if mode == "A":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:accesslist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ANYLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFANYLIST, channel.name, "Access")
		return 1

def access_on_join(client, channel):
	if not client.local:
		return
	if 'C' in client.user.modes:
		return
	opmode, _ = channel.has_access(client, 'A', "vhoa", 1)
	if opmode:
		Command.do(IRCD.me, "MODE", channel.name, *opmode.split(), *([client.name * 1]), str(channel.creationtime))

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_acclist)
	Hook.add(Hook.LOCAL_JOIN, access_on_join)
	Chmode_A = Channelmode()
	Chmode_A.flag = 'A'
	Chmode_A.sjoin_prefix = '^'
	Chmode_A.paramcount = 1
	Chmode_A.unset_with_param = 1
	Chmode_A.is_ok = acclist_change_permitted
	Chmode_A.level = 4
	Chmode_A.type = Channelmode.LISTMODE
	Chmode_A.param_help = '<vhoa>:<nick!ident@host>'
	Chmode_A.desc = 'Automatically ops the given hostmask on join'
	Channelmode.add(module, Chmode_A)
	Isupport.add("ACCLIST")
