"""
webirc support
"""
import ipaddress

from handle.core import IRCD, Command, Flag, Usermode, Hook
from handle.validate_conf import conf_error
from handle.core import logging
from handle.functions import address_inside_subnetlist, validate_cidr_addr


class WebIRCConf:
	password = None
	options = []
	ip_whitelist = []


def post_load(module):
	if not (webirc_settings := IRCD.configuration.get_items("settings:webirc")):
		return conf_error("WebIRC module is loaded but settings:webirc block is missing in configuration file")

	password = None
	for entry in webirc_settings:
		entry_name = entry.path[1]
		entry_value = entry.path[2]
		if entry_name == "password":
			password = entry_value
		if entry_name == "options":
			WebIRCConf.options.append(entry_value)
		if entry_name == "ip-whitelist":
			for ip in entry.get_path("ip-whitelist"):
				if ip in WebIRCConf.ip_whitelist:
					continue
				if not validate_cidr_addr(ip):
					conf_error(f"Invalid IP address '{ip}' in ip-whitelist of webirc module", item=entry)
					continue
				WebIRCConf.ip_whitelist.append(ip)

	if not password:
		return conf_error(f"settings:webirc:password missing or invalid")

	WebIRCConf.password = password


def webirc_add_umode(client):
	if client.user.webirc and 'v' not in client.user.modes:
		client.add_user_modes(['v'])


def init(module):
	Usermode.add(module, 'v', 1, 0, Usermode.allow_none, "User is connected through WebIRC")
	Command.add(module, cmd_webirc, "WEBIRC", 4, Flag.CMD_UNKNOWN)
	Hook.add(Hook.LOCAL_CONNECT, webirc_add_umode)


def cmd_webirc(client, recv):
	if client.registered or recv[1] != WebIRCConf.password or not address_inside_subnetlist(client.ip, WebIRCConf.ip_whitelist):
		return
	client.user.realhost = recv[3] if IRCD.get_setting("resolvehost") else recv[4]
	client.ip = recv[4]
	client.user.c_cloakhost = IRCD.get_cloak(client)
	client.user.cloakhost = client.user.realhost
	client.user.webirc = True
