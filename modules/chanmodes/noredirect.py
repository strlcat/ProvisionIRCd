"""
channel mode +F
"""

from handle.core import Channelmode


def init(module):
	Cmode_F = Channelmode()
	Cmode_F.flag = 'F'
	Cmode_F.paramcount = 0
	Cmode_F.is_ok = Channelmode.allow_chanadmin
	Cmode_F.desc = "Redirections to this channel are disabled"
	Channelmode.add(module, Cmode_F)
