"""
provides chmode +A (access/autoop list)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook, Isupport

HEADER = {
	"name": "channelaccess"
}

def display_acclist(client, channel, mode):
	if mode == "A":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:accesslist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ANYLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFANYLIST, channel.name, "Access")
		return 1

def access_on_join(client, channel):
	opmode = channel.has_access(client, 'A', "vhoa")
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
	Chmode_A.is_ok = Channelmode.allow_chanowner
	Chmode_A.level = 5
	Chmode_A.type = Channelmode.LISTMODE
	Chmode_A.param_help = '<vhoa>:<nick!ident@host>'
	Chmode_A.desc = 'Automatically ops the given hostmask on join'
	Channelmode.add(module, Chmode_A)
	Isupport.add("ACCLIST")
