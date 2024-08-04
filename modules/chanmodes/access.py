"""
provides chmode +A (access/autoop list)
"""

from handle.core import IRCD, Command, Numeric, Channelmode, Hook

HEADER = {
	"name": "channelaccess"
}


def display_acclist(client, channel, mode):
	if mode == "A":
		if channel.client_has_membermodes(client, "aq") or client.has_permission("channel:see:accesslist"):
			for entry in reversed(channel.List[mode]):
				client.sendnumeric(Numeric.RPL_ACCLIST, channel.name, entry.mask, entry.set_by, entry.set_time)
		client.sendnumeric(Numeric.RPL_ENDOFACCLIST, channel.name)
		return 1

def access_on_join(client, channel):
	opmode = channel.has_access(client)
	if opmode:
		Command.do(IRCD.me, "MODE", channel.name, *opmode.split(), *([client.name * 1]), str(channel.creationtime))

def init(module):
	Hook.add(Hook.CHAN_LIST_ENTRY, display_accesslist)
	Hook.add(Hook.LOCAL_JOIN, access_on_join)
	Chmode_b = Channelmode()
	Chmode_b.flag = 'A'
	Chmode_b.sjoin_prefix = '^'
	Chmode_b.paramcount = 1
	Chmode_b.unset_with_param = 1
	Chmode_b.is_ok = Channelmode.allow_chanowner
	Chmode_b.type = Channelmode.LISTMODE
	Chmode_b.param_help = '<vhoa>:<nick!ident@host>'
	Chmode_b.desc = 'Automatically ops the given hostmask on join'
	Channelmode.add(module, Chmode_b)
