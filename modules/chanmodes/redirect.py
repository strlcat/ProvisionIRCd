"""
channel mode +L
"""

from handle.core import IRCD, Channelmode, Numeric, Hook, Command, ChanPrivReq

def validate_redirect(client, channel, action, mode, param, CHK_TYPE):
	if CHK_TYPE == Channelmode.CHK_ACCESS:
		if channel.client_has_membermodes(client, "aq"):
			return ChanPrivReq.ACCESSOK
		return ChanPrivReq.NOTADMIN

	if CHK_TYPE == Channelmode.CHK_PARAM:
		if not IRCD.is_valid_channelname(param):
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"Invalid channel for redirect: {param}")
			return 0
		if not IRCD.find_channel(param):
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"Channel does not exist: {param}")
			return 0
		if (redirect_channel := IRCD.find_channel(param)) == channel:
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', "Channel cannot link to itself")
			return 0
		if 'L' in redirect_channel.modes:
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"Destination channel {param} already has +L set")
			return 0
		if not redirect_channel.find_member(client):
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"You must join {param} in order to link to it")
			return 0
		if not redirect_channel.client_has_membermodes(client, "aq"):
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"You must be channel admin or higher on {param} in order to link to it")
			return 0
		if 'F' in redirect_channel.modes:
			client.sendnumeric(Numeric.ERR_CANNOTCHANGECHANMODE, 'L', f"Destination channel {param} cannot be target for links")
			return 0
		return 1

	if (action == "+" and param.isdigit()) or (action == '-'):
		return 1
	return 0

def conv_param_redirect(param):
	return param

def sjoin_check_redirect(ourredirect, theirredirect):
	if ourredirect == theirredirect:
		# Same.
		return 0

	our_score = 0
	their_score = 0
	for char in ourredirect:
		our_score += ord(char)
	for char in theirredirect:
		their_score += ord(char)

	if our_score > their_score:
		return 1

def redirect_to_link(client, channel, error):
	if 'L' not in channel.modes:
		return
	if 'F' in client.user.modes:
		return
	link_chan = channel.get_param('L')
	if not (link_chan := IRCD.find_channel(link_chan)):
		return
	if 'L' in link_chan.modes:
		return

	Command.do(client, "JOIN", link_chan.name)

	match error:
		case Numeric.ERR_BANNEDFROMCHAN:
			IRCD.server_notice(client, f"You are banned from {channel.name} so you have been redirected to {link_chan.name}")
		case Numeric.ERR_INVITEONLYCHAN:
			IRCD.server_notice(client, f"Channel {channel.name} is invite-only so you have been redirected to {link_chan.name}")
		case Numeric.ERR_CHANNELISFULL:
			IRCD.server_notice(client, f"Channel {channel.name} is full so you have been redirected to {link_chan.name}")
		case Numeric.ERR_NEEDREGGEDNICK:
			IRCD.server_notice(client, f"Channel {channel.name} is for registered users only so you have been redirected to {link_chan.name}")
		case Numeric.ERR_SECUREONLY:
			IRCD.server_notice(client, f"Channel {channel.name} is for TLS-users only so you have been redirected to {link_chan.name}")
		case Numeric.ERR_OPERONLY:
			IRCD.server_notice(client, f"Channel {channel.name} is for IRC operators only so you have been redirected to {link_chan.name}")
		case _:
			IRCD.server_notice(client, f"Unable to join {channel.name}. You have been redirected to {link_chan.name}")

def init(module):
	Cmode_L = Channelmode()
	Cmode_L.flag = "L"
	Cmode_L.paramcount = 1
	Cmode_L.is_ok = validate_redirect
	Cmode_L.conv_param = conv_param_redirect
	Cmode_L.sjoin_check = sjoin_check_redirect
	Cmode_L.level = 4
	Cmode_L.unset_with_param = 1
	Cmode_L.param_help = "<channel>"
	Cmode_L.desc = "If a user is unable to join the channel, it will be redirected to the specified channel"
	Hook.add(Hook.JOIN_FAIL, redirect_to_link)
	Channelmode.add(module, Cmode_L)
