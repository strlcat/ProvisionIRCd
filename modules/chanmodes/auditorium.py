"""
channel mode +u
Users joining channel see only operators [+hoaq]
"""

from handle.core import Channelmode, Hook

def is_member_visible(user, target, channel):
	if 'u' in channel.modes:
		if user.name == target.name:
			return Hook.ALLOW
		if channel.client_has_membermodes(user, "oaq") or user.has_permission("channel:see:names"):
			return Hook.ALLOW
		elif channel.client_has_membermodes(target, "oaq"):
			return Hook.ALLOW
		return Hook.DENY
	return 0

def init(module):
	Hook.add(Hook.VISIBLE_ON_CHANNEL, is_member_visible)
	Cmode_u = Channelmode()
	Cmode_u.flag = 'u'
	Cmode_u.is_ok = Channelmode.allow_chanadmin
	Cmode_u.desc = "Users on channel can see only channel operators"
	Channelmode.add(module, Cmode_u)
