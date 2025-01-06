"""
channel mode +g (Libera chat free /invite)
"""

from handle.core import Channelmode


def init(module):
	Cmode_g = Channelmode()
	Cmode_g.flag = 'g'
	Cmode_g.paramcount = 0
	Cmode_g.is_ok = Channelmode.allow_chanop
	Cmode_g.desc = "Anybody in the channel can invite others"
	Channelmode.add(module, Cmode_g)
