"""
/lag command
"""

from handle.core import IRCD, Numeric, Command


def cmd_lag(client, recv):
	client.sendnumeric(Numeric.RPL_LAG, client.name, f"{round(client.lag)}")

def init(module):
	Command.add(module, cmd_lag, "LAG")
