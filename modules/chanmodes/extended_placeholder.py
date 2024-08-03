"""
channel mode +X (eXtended modes)
Currently a placeholder, not available to anyone.
Format: +X <extspec> <extparam>
"""

from handle.core import Channelmode

def conv_param_X(param):
	return param

def sjoin_check_X(a, b):
	return 1

def init(module):
	Cmode_X = Channelmode()
	Cmode_X.flag = "X"
	Cmode_X.paramcount = 2
	Cmode_X.is_ok = Channelmode.allow_none
	Cmode_X.conv_param = conv_param_X
	Cmode_X.sjoin_check = sjoin_check_X
	Cmode_X.sjoin_prefix = '#'
	Cmode_X.level = 7
	Cmode_X.unset_with_param = 1
	Cmode_X.type = Channelmode.LISTMODE
	Cmode_X.param_help = "<extspec> <extparam>"
	Cmode_X.desc = "Set extended arbitrary syntax channel modes. See /HELP XMODES (not implemented yet)"
	Channelmode.add(module, Cmode_X)
