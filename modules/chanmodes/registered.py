"""
channel mode +r
"""

from handle.core import Channelmode


def init(module):
	Cmode_r = Channelmode()
	Cmode_r.flag = 'r'
	Cmode_r.is_ok = Channelmode.allow_servbots
	Cmode_r.level = 7
	Cmode_r.desc = "Channel is registered"
	Channelmode.add(module, Cmode_r)
