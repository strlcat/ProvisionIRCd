"""
channel mode +D (no notices in the channel)
"""

from handle.core import Channelmode, Hook, Numeric


def can_channel_notice(client, channel, message, sendtype):
	if 'D' not in channel.modes or sendtype != "NOTICE":
		return Hook.ALLOW

	if not client.user or channel.client_has_membermodes(client, "hoaq") or client.has_permission("channel:override:message:notice"):
		return Hook.ALLOW

	client.sendnumeric(Numeric.ERR_CANNOTSENDTOCHAN, channel.name, "Notices are not permitted in this channel")
	return Hook.DENY


def init(module):
	Cmode_D = Channelmode()
	Cmode_D.flag = 'D'
	Cmode_D.is_ok = Channelmode.allow_halfop
	Cmode_D.desc = "Notices are not allowed in the channel"
	Channelmode.add(module, Cmode_D)
	Hook.add(Hook.CAN_SEND_TO_CHANNEL, can_channel_notice)
