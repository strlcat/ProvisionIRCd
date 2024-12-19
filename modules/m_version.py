"""
/version command
"""

from handle.core import IRCD, Command, Isupport, Numeric


def cmd_version(client, recv):
	client.sendnumeric(Numeric.RPL_VERSION, IRCD.version, IRCD.me.name, IRCD.hostinfo)
	Isupport.send_to_client(client)


def init(module):
	Command.add(module, cmd_version, "VERSION")
