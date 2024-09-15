"""
core user modes
"""
from handle.core import IRCD, Usermode, Snomask, Numeric

def umode_x_isok(client):
	if Usermode.allow_none(client):
		return 1
	chanlist = client.channels
	if len(chanlist) == 0:
		return 1
	if 'o' in client.user.modes:
		return 1
	client.sendnumeric(Numeric.ERR_CANNOTHIDEHOST)
	return 0

def umode_S_isok(client):
	if Usermode.allow_none(client):
		return 1
	if 'o' in client.user.modes and client.has_permission("self:become-service"):
		return 1
	return 0

def umode_q_isok(client):
	if Usermode.allow_none(client):
		return 1
	if 'o' in client.user.modes and client.has_permission("self:become-protected"):
		return 1
	return 0

def init(module):
	# Params: mode flag, is_global (will be synced to servers), unset_on_deoper bool, can_set method, desc
	Usermode.add(module, 'i', 1, 0, Usermode.allow_all, "User does not show up in outside /who")
	Usermode.add(module, 'o', 1, 1, Usermode.allow_opers, "Marks the user as an IRC Operator")
	Usermode.add(module, 'q', 1, 1, umode_q_isok, "Protected on all channels")
	Usermode.add(module, 'r', 1, 0, Usermode.allow_services, "Identifies the nick as being logged in")
	Usermode.add(module, 's', 1, 1, Usermode.allow_opers, "Can receive server notices")
	Usermode.add(module, "x", 1, 0, umode_x_isok, "Hides real host with cloaked host")
	Usermode.add(module, 'X', 0, 0, Usermode.allow_none, "Extended usermodes are in effect (reserved for future use)")
	Usermode.add(module, 'z', 1, 0, Usermode.allow_none, "User is using a secure connection")
	Usermode.add(module, 'H', 1, 1, Usermode.allow_opers, "Hide IRCop status")
	Usermode.add(module, 'S', 1, 1, umode_S_isok, "Client acts as a network service [Settable by services]")

	Snomask.add(module, 'c', 0, "Can read local connect/disconnect notices")
	Snomask.add(module, 'f', 1, "See excess flood alerts")
	Snomask.add(module, 'k', 0, "View kill notices")
	Snomask.add(module, 'o', 1, "See oper-up notices")
	Snomask.add(module, 's', 0, "General server notices")
	Snomask.add(module, 'C', 0, "Can read global connect/disconnect notices")
	Snomask.add(module, 'F', 1, "View spamfilter matches")
	Snomask.add(module, 'G', 0, "View TKL usages")
	Snomask.add(module, 'L', 0, "View server notices about links")
	Snomask.add(module, 'N', 0, "Can see nick changes")
	Snomask.add(module, 'Q', 1, "View Q:line rejections")
	Snomask.add(module, 'S', 0, "Can see /sanick, /sajoin, and /sapart usage")
