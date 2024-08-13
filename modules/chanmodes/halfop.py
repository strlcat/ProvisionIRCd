"""
halfop
"""

import logging

from handle.core import Channelmode, ChanPrivReq, IRCD
from handle.functions import compare_chanops

def validate_member(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		# Access will be performed actually by CHK_MEMBER later
		return ChanPrivReq.ACCESSOK
	elif CHK_TYPE == Channelmode.CHK_MEMBER:
		if target := IRCD.find_user(param):
			if action in "-+" and ((channel.client_has_membermodes(client, "oaq") and compare_chanops(channel, client, target) >= 0) or not client.local):
				return ChanPrivReq.ACCESSOK
			# Cannot do -h on anyone but myself
			if action == '-' and target.name == client.name and channel.client_has_membermodes(client, "h"):
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
