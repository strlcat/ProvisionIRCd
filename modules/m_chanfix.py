"""
commands /chanfix, /chown, /disown, /founder and /opme
Restore operator (or whatever default join empty privilege) on channel
"""

from handle.core import Flag, Numeric, Command, IRCD


def cmd_chanfix(client, recv):
	"""
	Syntax: CHANFIX <channel>
	Restores lost owner status on given channel.
	You must be a creator of the channel in order
	to restore owner status on it. If channel is
	registered (+r), CHANFIX is disabled on it.
	"""
	if not client.local:
		return

	IRCD.new_message(client)
	if not IRCD.get_setting("chanfix"):
		IRCD.server_notice(client, "Sorry, CHANFIX is not available on this server. Ask IRC operators for help")
		return

	chname = recv[1]
	channel = IRCD.find_channel(chname)
	if not channel:
		client.sendnumeric(Numeric.ERR_NOSUCHCHANNEL, chname)
		return
	if not channel.find_member(client):
		client.sendnumeric(Numeric.ERR_NOTONCHANNEL, chname)
		return

	if 'r' in channel.modes:
		IRCD.server_notice(client, f"CHANFIX is disabled for {chname} because it is registered (+r)")
		return

	# Ok let's try to restore privs for the guy.
	if not channel.do_chanfix_check(client):
		IRCD.server_notice(client, f"CHANFIX: {chname} seems not to be yours, sorry.")
	else:
		channel.do_chanfix(client)
		IRCD.server_notice(client, f"CHANFIX: restored your {chname}, consider registering it")

def cmd_chown(client, recv):
	"""
	Syntax: CHOWN <channel> <target>
	If target nickname is online, CHOWN will transfer
	founder status of <channel> to the <target>.
	Later, <target> can use /CHANFIX to restore privileges
	of that channel.
	It will not work with registered (+r) channels.
	Query services about gaining access on registered channel.
	"""
	if not client.local:
		return

	IRCD.new_message(client)
	if not IRCD.get_setting("chanfix"):
		IRCD.server_notice(client, "Sorry, CHANFIX is not available on this server. Ask IRC operators for help")
		return

	chname = recv[1]
	uname = recv[2]
	channel = IRCD.find_channel(chname)
	if not channel:
		client.sendnumeric(Numeric.ERR_NOSUCHCHANNEL, chname)
		return

	if 'r' in channel.modes:
		IRCD.server_notice(client, f"CHANFIX is disabled for {chname} because it is registered (+r)")
		return

	target = IRCD.find_user(uname)
	if not target:
		client.sendnumeric(Numeric.ERR_NOSUCHNICK, uname)
		return

	if not channel.do_chanfix_check(client) and not client.has_permission("channel:override:chown"):
		IRCD.server_notice(client, f"CHANFIX: {chname} seems not to be yours, sorry.")
		return

	# Ok to chown, let's do it
	channel.founder = IRCD.channel_founder_fingerprint(target)
	IRCD.server_notice(client, f"CHANFIX: {chname} ownership was transferred to {uname}")

def cmd_disown(client, recv):
	"""
	Syntax: DISOWN <channel>
	Give up channel ownership to void. You must be owner to give up channel.
	CHANFIX then will never will be able to restore channel privileges
	for you on that channel. You have either to register it, or ensure
	ownership of channel you own will be somehow secured. It is up to you.
	It will not work with registered (+r) channels.
	"""
	if not client.local:
		return

	IRCD.new_message(client)
	if not IRCD.get_setting("chanfix"):
		IRCD.server_notice(client, "Sorry, CHANFIX is not available on this server. Ask IRC operators for help")
		return

	chname = recv[1]
	channel = IRCD.find_channel(chname)
	if not channel:
		client.sendnumeric(Numeric.ERR_NOSUCHCHANNEL, chname)
		return

	if 'r' in channel.modes:
		IRCD.server_notice(client, f"CHANFIX is disabled for {chname} because it is registered (+r)")
		return

	# Ok let's try to relinquish privs of the channel.
	if not channel.do_chanfix_check(client):
		IRCD.server_notice(client, f"CHANFIX: {chname} seems not to be yours, sorry.")
	else:
		channel.founder = ''
		IRCD.server_notice(client, f"CHANFIX: now {chname} is abandoned")

def cmd_founder(client, recv):
	"""
	Syntax: FOUNDER <channel>
	Retrieves full mask or certfp of channel creator, if available.
	Registered channels (+r) will return "Not applicable".
	"""
	if not client.local:
		return

	IRCD.new_message(client)
	if not IRCD.get_setting("chanfix"):
		IRCD.server_notice(client, "CHANFIX is disabled.")
		return

	if not client.has_permission("channel:see:creator"):
		client.sendnumeric(Numeric.ERR_NOPRIVILEGES)
		return

	chname = recv[1]
	channel = IRCD.find_channel(chname)
	if not channel:
		client.sendnumeric(Numeric.ERR_NOSUCHCHANNEL, chname)
		return

	if 'r' in channel.modes:
		founder_info = "Not applicable (+r)"
	else:
		founder_info = channel.founder

	if not founder_info:
		founder_info = "Not owned by anyone (?)"

	IRCD.server_notice(client, f"Founder of {chname}: {founder_info}")

def cmd_opme(client, recv):
	"""
	Syntax: OPME <channel>
	Forces server to scan channel access list (+A), and if
	access entry is found for your hostmask, grants you privilege
	specified by that access entry (+vhoa), or highest privilege
	in case if multiple access hostmasks match yours.
	Does nothing if no entry was found.
	"""
	if not client.local:
		return

	IRCD.new_message(client)

	chname = recv[1]
	channel = IRCD.find_channel(chname)
	if not channel:
		client.sendnumeric(Numeric.ERR_NOSUCHCHANNEL, chname)
		return
	if not channel.find_member(client):
		client.sendnumeric(Numeric.ERR_NOTONCHANNEL, chname)
		return
	# Scan & restore privs according to channel +A entries
	opmode = channel.has_access(client)
	if opmode:
		Command.do(IRCD.me, "MODE", channel.name, *opmode.split(), *([client.name * 1]), str(channel.creationtime))
		IRCD.server_notice(client, f"{chname}: granted access +{opmode} {client.name}")
	else:
		IRCD.server_notice(client, f"{chname}: no access entry is found for your hostmask.")

def init(module):
	Command.add(module, cmd_chanfix, "CHANFIX", 1, Flag.CMD_USER)
	Command.add(module, cmd_chown, "CHOWN", 2, Flag.CMD_USER)
	Command.add(module, cmd_disown, "DISOWN", 1, Flag.CMD_USER)
	Command.add(module, cmd_founder, "FOUNDER", 1, Flag.CMD_OPER)
	Command.add(module, cmd_opme, "OPME", 1, Flag.CMD_USER)
