"""
channel mode +k
"""

from handle.core import IRCD, Numeric, Flag, Command, Channelmode, Hook, ChanPrivReq
from handle.functions import hash_data, b2h_upper, xor_shrink, isxdigit

def is_hashed_key(keystr):
	if len(keystr) == 16 and keystr.isalnum and keystr.isupper():
		return True
	return False

def hash_key(key):
	cloak_key = IRCD.get_setting("cloak-key")
	h = hash_data(cloak_key, bytes(key, "utf-8"))
	hsh = xor_shrink(h, 8)
	r = b2h_upper(hsh)
	return r

def key_is_ok(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		if channel.client_has_membermodes(client, "aq"):
			return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTADMIN

	if CHK_TYPE == Channelmode.CHK_PARAM:
		for char in param:
			if not char.isalpha() and not char.isdigit():
				client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'k', '*', f"Key contains invalid character: {char}")
				return 0
		return 1
	return 0

def can_join_key(client, channel, key):
	if client.has_permission("channel:override:join:key"):
		return 0
	if channel.is_owner(client):
		return 0
	if 'k' in channel.modes:
		if key == None or key == "":
			return Numeric.ERR_BADCHANNELKEY
		chankey = channel.get_param('k')
		if is_hashed_key(chankey) and hash_key(key) == chankey:
			return 0
		if key == chankey:
			return 0
		return Numeric.ERR_BADCHANNELKEY
	return 0

def key_conv_param(param):
	return param[:24]

def sjoin_check_key(ourkey, theirkey):
	if ourkey == theirkey:
		# Same.
		return 0

	our_score = 0
	their_score = 0
	for char in ourkey:
		our_score += ord(char)
	for char in theirkey:
		their_score += ord(char)

	if our_score > their_score:
		return 1

	return -1

def cmd_makekey(client, recv):
	IRCD.server_notice(client, f"* hashed key is: {hash_key(recv[1])}")

def init(module):
	Cmode_k = Channelmode()
	Cmode_k.flag = "k"
	Cmode_k.paramcount = 1
	Cmode_k.unset_with_param = 1
	Cmode_k.is_ok = key_is_ok
	Cmode_k.conv_param = key_conv_param
	Cmode_k.sjoin_check = sjoin_check_key
	Cmode_k.param_help = "<key>"
	Cmode_k.desc = "Channel requires a key to join"
	Cmode_k.level = 4
	Channelmode.add(module, Cmode_k)
	Hook.add(Hook.CAN_JOIN, can_join_key)
	Command.add(module, cmd_makekey, "MAKEKEY", 1, Flag.CMD_USER)
