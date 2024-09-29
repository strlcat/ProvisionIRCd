"""
nginx PROXY v1 support
"""
import ipaddress

from handle.core import IRCD, Command, Flag, Usermode, Hook
from handle.validate_conf import conf_error
from handle.core import logging
from handle.functions import address_inside_subnetlist, validate_cidr_addr


class NginxPROXYConf:
	external_addresses = []
	external_tls_ports = []
	ip_whitelist = []


def post_load(module):
	if not (ngxproxy_settings := IRCD.configuration.get_items("settings:ngxproxy")):
		return conf_error("Nginx PROXY module is loaded but settings:ngxproxy block is missing in configuration file")

	for entry in ngxproxy_settings:
		entry_name = entry.path[1]
		entry_value = entry.path[2]
		if entry_name == "external-address":
			for ip in entry.get_path("external-address"):
				if ip in NginxPROXYConf.external_addresses:
					continue
				if not validate_cidr_addr(ip):
					conf_error(f"Invalid IP address '{ip}' in external-address of ngxproxy module", item=entry)
					continue
				NginxPROXYConf.external_addresses.append(ip)
		if entry_name == "external-tls-port":
			NginxPROXYConf.external_tls_ports.append(entry_value)
		if entry_name == "ip-whitelist":
			for ip in entry.get_path("ip-whitelist"):
				if ip in NginxPROXYConf.ip_whitelist:
					continue
				if not validate_cidr_addr(ip):
					conf_error(f"Invalid IP address '{ip}' in ip-whitelist of ngxproxy module", item=entry)
					continue
				NginxPROXYConf.ip_whitelist.append(ip)


def ngxproxytls_add_umode(client):
	if client.user.ngxproxytls and 'z' not in client.user.modes:
		client.add_user_modes(['z'])


def init(module):
	# PROXY TCP4 127.1.2.3 127.0.0.1 42640 6667
	# PROXY TCP6 2001:470:db8:7a4e::6667 2002:9a9a:a9a9::9a9a:a9a9 42640 6697
	Command.add(module, cmd_ngxproxy, "PROXY", 5, Flag.CMD_UNKNOWN)
	Hook.add(Hook.LOCAL_CONNECT, ngxproxytls_add_umode)


def cmd_ngxproxy(client, recv):
	if client.registered or not address_inside_subnetlist(client.ip, NginxPROXYConf.ip_whitelist):
		return
	if recv[1] not in ["TCP4", "TCP6"]:
		return
	if len(NginxPROXYConf.external_addresses) > 0 and not address_inside_subnetlist(recv[3], NginxPROXYConf.external_addresses):
		return
	client.user.realhost = recv[2]
	client.ip = recv[2]
	client.port = recv[4]
	extport = recv[5]
	if extport in NginxPROXYConf.external_tls_ports:
		client.user.ngxproxytls = True
	if IRCD.get_setting("resolvehost"):
		try:
			realhost = gethostbyaddr(client.ip)[0]
			if realhost == "localhost" and not ipaddress.IPv4Address(client.ip).is_private:
				raise Exception
			client.user.realhost = realhost
			IRCD.server_notice(client, f"*** Found your hostname: {client.user.realhost}")
		except:
			client.user.realhost = client.ip
			IRCD.server_notice(client, f"*** Couldn't resolve your hostname, using IP address instead")
	client.user.c_cloakhost = IRCD.get_cloak(client)
	client.user.cloakhost = client.user.realhost
	logging.debug(f"Client [{client.ip}]:{client.port} connected using nginx PROXY [{recv[3]}]:{recv[5]} with UID: {client.id}")
