"""
chanop
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
			# Cannot do -o on anyone but myself
			if action == '-' and target.name == client.name and channel.client_has_membermodes(client, "o"):
				return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOPER
	return 0

def init(module):
	Cmode_o = Channelmode()
	Cmode_o.flag = 'o'
	Cmode_o.prefix = '@'
	Cmode_o.sjoin_prefix = '@'
	Cmode_o.paramcount = 1
	Cmode_o.unset_with_param = 1
	Cmode_o.type = Channelmode.MEMBER
	Cmode_o.rank = 200  # Used to determine the position in PREFIX Isupport
	Cmode_o.level = 3
	Cmode_o.is_ok = validate_member
	Cmode_o.desc = "Give/take operator status"
	Channelmode.add(module, Cmode_o)
