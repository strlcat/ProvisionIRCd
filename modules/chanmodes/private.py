"""
channel mode +p
"""

from handle.core import Channelmode


def init(module):
	Cmode_p = Channelmode()
	Cmode_p.flag = 'p'
	Cmode_p.paramcount = 0
	Cmode_p.is_ok = Channelmode.allow_chanop
	Cmode_p.desc = "Private channel, removes details from /list and disables /knock"
	Channelmode.add(module, Cmode_p)
