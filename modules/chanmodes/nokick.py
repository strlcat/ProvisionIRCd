"""
channel mode +Q
"""

from handle.core import Channelmode


def init(module):
	Cmode_Q = Channelmode()
	Cmode_Q.flag = 'Q'
	Cmode_Q.paramcount = 0
	Cmode_Q.is_ok = Channelmode.allow_chanadmin
	Cmode_Q.desc = "Only channel admins or above can /KICK users from channel"
	Channelmode.add(module, Cmode_Q)
