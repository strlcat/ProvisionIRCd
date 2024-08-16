"""
channel mode +U (channel settings cannot be changed by inferior opers)
"""

from handle.core import Channelmode, ChanPrivReq, Numeric

def validate_param_rdonly(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		if channel.client_has_membermodes(client, "q"):
			return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTOWNER

	if CHK_TYPE == Channelmode.CHK_PARAM:
		if len(param) > 1:
			client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'U', '*', "Parameter too long, must be a single character from: 'qaoh'")
			return 0
		for c in param:
			if c not in 'qaoh':
				client.sendnumeric(Numeric.ERR_INVALIDMODEPARAM, channel.name, 'U', '*', f"Operator mode {c} is invalid, must be from: 'qaoh'")
				return 0
		return 1
	return 0

def rdonly_conv_param(param):
	return param[:1]

def sjoin_check_rdonly(ourflag, theirflag):
	if ourflag == theirflag:
		# Same.
		return 0

	our_score = 0
	their_score = 0
	for char in ourflag:
		our_score += ord(char)
	for char in theirflag:
		their_score += ord(char)

	if our_score > their_score:
		return 1
	return -1

def init(module):
	Cmode_U = Channelmode()
	Cmode_U.flag = 'U'
	Cmode_U.paramcount = 1
	Cmode_U.is_ok = validate_param_rdonly
	Cmode_U.conv_param = rdonly_conv_param
	Cmode_U.sjoin_check = sjoin_check_rdonly
	Cmode_U.level = 5
	Cmode_U.param_help = "<qaoh>"
	Cmode_U.desc = "Restrict changing channel modes to channel operator class"
	Channelmode.add(module, Cmode_U)
