"""
/lag command
"""
from time import time
from handle.core import IRCD, Numeric, Command, Hook, Flag


def cmd_lag(client, recv):
	"""
	Syntax: LAG
	Pings server and returns result delay in milliseconds.
	"""
	# Shall we completely ignore immutable users with umode +p?
	target = client
	if len(recv) > 1:
		if not 'o' in client.user.modes:
			target.sendnumeric(Numeric.ERR_NOPRIVILEGES)
			return
		target = IRCD.find_user(recv[1])
		if not target:
			client.sendnumeric(Numeric.ERR_NOSUCHNICK, recv[1])
			return
		if target.is_service:
			IRCD.server_notice(client, "*** You cannot use /LAG on services.")
			return
		target.operated_by = client
	target.reply_to_lag = True
	target.send([], f"PING :{IRCD.me.name}")
	target.last_ping_sent = time() * 1000

def reply_lag(client, arg):
	if not client.reply_to_lag:
		return
	client.reply_to_lag = False
	client.lag = (time() * 1000) - client.last_ping_sent
	target = client
	if client.operated_by:
		target = client.operated_by
		client.operated_by = None
	target.sendnumeric(Numeric.RPL_LAG, client.name, f"{round(client.lag)}")

def init(module):
	Command.add(module, cmd_lag, "LAG", 0, Flag.CMD_USER)
	Hook.add(Hook.PONG, reply_lag)
