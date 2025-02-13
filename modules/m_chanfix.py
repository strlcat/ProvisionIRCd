"""
commands /chanfix, /chown, /disown, /founder and /opme
Restore operator (or whatever default join empty privilege) on channel
"""

from handle.core import Flag, Numeric, Command, IRCD, Hook, Usermode


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
	if not channel.is_owner(client):
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
	If channel is abandoned, you can gain ownership over it
	by /CHOWNing to yourself, but it will work only on
	unregistered channels.
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

	if channel.is_owner(client) or client.has_permission("channel:override:chown") or len(channel.founder) == 0:
		if len(channel.founder) == 0 and client.name.lower() != target.name.lower():
			IRCD.server_notice(client, f"CHANFIX: {chname} is abandoned, but try to chown it to yourself first.")
			return

		# Ok to chown, let's do it
		if channel.find_member(client) and channel.client_has_membermodes(client, "q"):
			Command.do(IRCD.me, "MODE", channel.name, *"-q".split(), *([client.name * 1]), str(channel.creationtime))
		if channel.find_member(target) and not channel.client_has_membermodes(target, "q"):
			Command.do(IRCD.me, "MODE", channel.name, *"+q".split(), *([target.name * 1]), str(channel.creationtime))

		channel.founder = IRCD.channel_founder_fingerprint(target)
		broadcast_schown(client, channel.name, channel.founder)
		IRCD.server_notice(client, f"CHANFIX: {chname} ownership was transferred to {uname}")
	else:
		IRCD.server_notice(client, f"CHANFIX: {chname} seems not to be yours, sorry.")

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
	if channel.is_owner(client) or client.has_permission("channel:override:chown"):
		if channel.find_member(client) and channel.client_has_membermodes(client, "q"):
			Command.do(IRCD.me, "MODE", channel.name, *"-q".split(), *([client.name * 1]), str(channel.creationtime))

		channel.founder = ''
		broadcast_schown(client, channel.name, channel.founder)
		IRCD.server_notice(client, f"CHANFIX: now {chname} is abandoned")
	else:
		IRCD.server_notice(client, f"CHANFIX: {chname} seems not to be yours, sorry.")

def cmd_founder(client, recv):
	"""
	Syntax: FOUNDER <channel>
	Retrieves full certfp/account/hostmask of channel creator, if available.
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
	opmode, _ = channel.has_access(client, 'A', "vhoa", 1)
	if opmode:
		Command.do(IRCD.me, "MODE", channel.name, *opmode.split(), *([client.name * 1]), str(channel.creationtime))
		IRCD.server_notice(client, f"{chname}: granted access +{opmode} {client.name}")
	else:
		IRCD.server_notice(client, f"{chname}: no access entry is found for your hostmask.")

def broadcast_schown(client, channel):
	if len(channel.founder) == 0:
		foundermask = "*"
	else:
		foundermask = channel.founder
	data = f":{client.uplink.id} SCHOWN {channel.name} {foundermask} {channel.creationtime}"
	IRCD.send_to_servers(client, [], data)

def cmd_schown(client, recv):
	chname = recv[1]
	hostmask = recv[2]
	chctime = recv[3]

	channel = IRCD.find_channel(chname)
	if not channel:
		return

	if 'r' in channel.modes:
		channel.founder = ''
		return

	if hostmask == "*":
		channel.founder = ''
		return

	if int(chctime) >= channel.creationtime:
		return

	channel.founder = hostmask

def hook_schown(client, channel):
	broadcast_schown(client, channel)

def init(module):
	Usermode.add(module, 'C', 1, 0, Usermode.allow_all, "Automatic oper up and CHANFIX is disabled")
	Command.add(module, cmd_chanfix, "CHANFIX", 1, Flag.CMD_USER)
	Command.add(module, cmd_chown, "CHOWN", 2, Flag.CMD_USER)
	Command.add(module, cmd_disown, "DISOWN", 1, Flag.CMD_USER)
	Command.add(module, cmd_founder, "FOUNDER", 1, Flag.CMD_OPER)
	Command.add(module, cmd_opme, "OPME", 1, Flag.CMD_USER)
	Command.add(module, cmd_schown, "SCHOWN", 3, Flag.CMD_SERVER)
	Hook.add(Hook.CHANNEL_CREATE, hook_schown)
