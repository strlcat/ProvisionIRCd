"""
unregistered bans/exceptions/invex
~unregistered:mask
"""

from handle.core import IRCD, Extban
from handle.functions import is_match, make_mask

HEADER = {
	"name": "extbans/unregistered"
}

def unregistered_is_valid(client, channel, action, mode, param):
	param_split = param.split(':')
	if len(param_split) < 2 or len(param_split) > 40:
		return 0
	banmask = make_mask(':'.join(param_split[1:]))
	param = f"{':'.join(param_split[:-1])}:{banmask}"
	return param

def unregistered_is_match(client, channel, mask):
	"""mask == raw ban entry from a channel"""
	if 'r' in client.user.modes and client.user.account != "*":
		return 0
	split_mask = mask.split(':')
	if len(split_mask) < 2 or len(split_mask) > 40:
		return 0
	umask = ':'.join(split_mask[1:])
	if (channel.check_match(client, 'b', umask) or channel.check_match(client, 'B', umask)) and not channel.is_exempt(client):
		return 1
	if channel.is_invex(client):
		return 1
	return 0

class UnregisteredExtban:
	name = "unreg"
	flag = "U"
	paramcount = 1
	is_ok = unregistered_is_valid
	is_match = unregistered_is_match

def init(module):
	Extban.add(UnregisteredExtban)
