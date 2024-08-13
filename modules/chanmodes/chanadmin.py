"""
chanadmin (+a)
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
			if action in "-+" and ((channel.client_has_membermodes(client, "q") and compare_chanops(channel, client, target) == 1) or not client.local):
				return ChanPrivReq.ACCESSOK
			# Cannot do -a on anyone but myself
			if action == '-' and target.name == client.name and channel.client_has_membermodes(client, "a"):
				return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOWNER
	return 0

def init(module):
	Cmode_a = Channelmode()
	Cmode_a.flag = 'a'
	Cmode_a.prefix = '&'
	Cmode_a.sjoin_prefix = '~'
	Cmode_a.paramcount = 1
	Cmode_a.unset_with_param = 1
	Cmode_a.type = Channelmode.MEMBER
	Cmode_a.rank = 300  # Used to determine the position in PREFIX Isupport
	Cmode_a.level = 4
	Cmode_a.is_ok = validate_member
	Cmode_a.desc = "Give/take channel admin status"
	Channelmode.add(module, Cmode_a)
