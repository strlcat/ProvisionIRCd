"""
halfop
"""

import logging

from handle.core import Channelmode, ChanPrivReq

def validate_member(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		if action in "-+" and (channel.client_has_membermodes(client, "oaq") or not client.local):
			return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOPER
	return 0

def init(module):
	Cmode_h = Channelmode()
	Cmode_h.flag = 'h'
	Cmode_h.prefix = '%'
	Cmode_h.sjoin_prefix = '%'
	Cmode_h.paramcount = 1
	Cmode_h.unset_with_param = 1
	Cmode_h.type = Channelmode.MEMBER
	Cmode_h.rank = 100  # Used to determine the position in PREFIX Isupport
	Cmode_h.level = 3
	Cmode_h.is_ok = validate_member
	Cmode_h.desc = "Give/take channel halfop status"
	Channelmode.add(module, Cmode_h)
