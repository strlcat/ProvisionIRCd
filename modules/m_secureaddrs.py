"""
assume the following ip addresses are always secure
"""
import ipaddress

from handle.core import IRCD, Hook
from handle.validate_conf import conf_error
from handle.functions import address_inside_subnetlist, validate_cidr_addr

class secureaddrs:
	addrlist = []

def post_load(module):
	if not (addrs := IRCD.get_setting("secureaddrs")):
		return conf_error(f"secureaddrs module loaded but settings:secureaddrs block is missing")
	for addr in addrs:
		if not validate_cidr_addr(addr):
			return conf_error(f"IP address {addr} is not valid in secureaddrs list")
	secureaddrs.addrlist = addrs

def secureaddrs_mark_as_secure(client):
	if address_inside_subnetlist(client.ip, secureaddrs.addrlist):
		if 'z' not in client.user.modes:
			client.secure = True
			client.add_user_modes(['z'])

def init(module):
	Hook.add(Hook.LOCAL_CONNECT, secureaddrs_mark_as_secure, 210)
