"""
channel bans/exceptions/invex
~channel:mask
"""

from handle.core import IRCD, Extban
from handle.functions import is_match, make_mask

HEADER = {
	"name": "extbans/channel"
}

def channel_is_valid(client, channel, action, mode, param):
	param_split = param.split(':')
	if len(param_split) != 2:
		return 0
	if param_split[1][0] not in IRCD.CHANPREFIXES:
		return 0
	return param

def channel_is_match(client, channel, mask):
	"""mask == raw ban entry from a channel"""
	if len(client.user.channels) == 0:
		return 0
	split_mask = mask.split(':')
	if len(split_mask) != 2:
		return 0
	channel = split_mask[1]
	for c in client.user.channels:
		if c.name.lower() == channel.lower():
			return 1
	return 0

class ChannelExtban:
	name = "channel"
	flag = "c"
	paramcount = 1
	is_ok = channel_is_valid
	is_match = channel_is_match

def init(module):
	Extban.add(ChannelExtban)
