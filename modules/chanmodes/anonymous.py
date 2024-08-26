"""
channel mode +U
Users chatting in channel cannot see real nicknames, except of channel operators
"""

from handle.core import Channelmode, Hook

def init(module):
	Cmode_U = Channelmode()
	Cmode_U.flag = 'U'
	Cmode_U.is_ok = Channelmode.allow_chanadmin
	Cmode_U.desc = "All chat lines on channel are anonymized, except of channel operators"
	Channelmode.add(module, Cmode_U)
