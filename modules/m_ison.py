"""
/ison, /userhost and /userip command
"""

from handle.core import Numeric, Command, IRCD


def cmd_ison(client, recv):
	"""
	Checks to see if a nickname is online.
	Example: /ISON Nick1 SomeOthernick
	"""

	nicks = []
	for nick in recv[1:]:
		for u_client in [u_client for u_client in IRCD.global_users() if u_client.name.lower() == nick.lower() and u_client.name not in nicks]:
			nicks.append(u_client.name)
	client.sendnumeric(Numeric.RPL_ISON, ' '.join(nicks))


def cmd_userhost(client, recv):
	"""
	Returns the cloaked (or, if permitted, real) userhost of the given user.
	Example: /USERHOST John
	"""

	hosts = []
	for nick in recv[1:]:
		for u_client in [u_client for u_client in IRCD.global_users() if u_client.name.lower() == nick.lower() and u_client.name not in hosts]:
			if client.has_permission("client:see:hosts") or client.name.lower() == nick.lower():
				h = f"{u_client.name}*=+{u_client.user.username}@{u_client.user.realhost}"
			else:
				h = f"{u_client.name}*=+{u_client.user.username}@{u_client.user.cloakhost}"
			if h not in hosts:
				hosts.append(h)
	client.sendnumeric(Numeric.RPL_USERHOST, ' '.join(hosts))


def cmd_userip(client, recv):
	"""
	Returns the cloaked (or, if permitted, real) userip of the given user.
	Example: /USERIP John
	"""

	hosts = []
	for nick in recv[1:]:
		for u_client in [u_client for u_client in IRCD.global_users() if u_client.name.lower() == nick.lower() and u_client.ip not in hosts]:
			if client.has_permission("client:see:hosts") or client.name.lower() == nick.lower():
				h = f"{u_client.ip}"
			else:
				h = f"{u_client.user.cloakhost}"
			if h not in hosts:
				hosts.append(h)
	client.sendnumeric(Numeric.RPL_USERIP, ' '.join(hosts))


def init(module):
	Command.add(module, cmd_ison, "ISON", 1)
	Command.add(module, cmd_userhost, "USERHOST", 1)
	Command.add(module, cmd_userip, "USERIP", 1)
