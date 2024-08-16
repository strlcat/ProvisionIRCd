"""
channel mode +U (channel settings cannot be changed)
"""

from handle.core import Channelmode


def init(module):
	Cmode_U = Channelmode()
	Cmode_U.flag = 'U'
	Cmode_U.is_ok = Channelmode.allow_chanowner
	Cmode_U.desc = "Channel modes can be changed only by channel founder"
	Channelmode.add(module, Cmode_U)
