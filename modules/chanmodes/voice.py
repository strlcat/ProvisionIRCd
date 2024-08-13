"""
voice
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
			if action in "-+" and ((channel.client_has_membermodes(client, "hoaq") and compare_chanops(channel, client, target) >= 0) or not client.local):
				return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOPER
	return 0

def init(module):
	Cmode_v = Channelmode()
	Cmode_v.flag = 'v'
	Cmode_v.prefix = '+'
	Cmode_v.sjoin_prefix = '+'
	Cmode_v.paramcount = 1
	Cmode_v.unset_with_param = 1
	Cmode_v.type = Channelmode.MEMBER
	Cmode_v.rank = 1  # Used to determine the position in PREFIX Isupport
	Cmode_v.is_ok = validate_member
	Cmode_v.desc = "Give/take channel voice status"
	Channelmode.add(module, Cmode_v)
