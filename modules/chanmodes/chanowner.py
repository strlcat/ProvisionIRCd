"""
chanowner (+q)
"""

import logging

from handle.core import Channelmode, ChanPrivReq, IRCD

def validate_member(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		# Access will be performed actually by CHK_MEMBER later
		return ChanPrivReq.ACCESSOK
	elif CHK_TYPE == Channelmode.CHK_MEMBER:
		if action in "-+" and not client.local:
			return ChanPrivReq.ACCESSOK
		# Only one owner can be on channel
		if action == "+" and (channel.client_has_membermodes(client, "q") or not client.local):
			return ChanPrivReq.ONLYOWNER
		if target := IRCD.find_user(param):
			# Cannot do -q on anyone but myself
			if action == '-' and target.name == client.name and channel.client_has_membermodes(client, "q"):
				return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOWNER
	return 0

def init(module):
	Cmode_q = Channelmode()
	Cmode_q.flag = 'q'
	Cmode_q.prefix = '~'
	Cmode_q.sjoin_prefix = '*'
	Cmode_q.paramcount = 1
	Cmode_q.unset_with_param = 1
	Cmode_q.type = Channelmode.MEMBER
	Cmode_q.rank = 400  # Used to determine the position in PREFIX Isupport
	Cmode_q.level = 5
	Cmode_q.is_ok = validate_member
	Cmode_q.desc = "Give/take channel owner status"
	Channelmode.add(module, Cmode_q)
