"""
channel mode +V
"""

from handle.core import Channelmode


def init(module):
	Cmode_V = Channelmode()
	Cmode_V.flag = 'V'
	Cmode_V.is_ok = Channelmode.allow_chanadmin
	Cmode_V.desc = "Only channel admins (+a) or higher can /INVITE to the channel"
	Channelmode.add(module, Cmode_V)
