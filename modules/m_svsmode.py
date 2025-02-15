"""
/svsmode, /svs2mode and /svssno command (server)
"""

from handle.core import IRCD, Command, Flag, Hook
from handle.functions import logging
from modules.m_kick import do_kick


def cmd_svsmode(client, recv):
	if not (target := IRCD.find_user(recv[1])):
		return

	action = ''
	modes = ''
	oldumodes = target.user.modes
	for m in recv[2]:
		if m in '+-' and m != action:
			action = m
			modes += action
			continue

		if m != "d" and m not in IRCD.get_umodes_str():
			continue

		if m == "d":  # Set or remove account.
			if len(recv) > 3:
				account = recv[3]
				curr_account = target.user.account
				target.user.account = account if account != "0" else "*"
				if curr_account != account:
					IRCD.run_hook(Hook.ACCOUNT_LOGIN, target)
				continue
			elif m not in IRCD.get_umodes_str():
				continue

		if action == '+':
			if m not in target.user.modes:
				if m == 'x':
					target.setinfo(info=target.user.c_cloakhost, t="host")
					data = f":{target.id} SETHOST :{target.user.cloakhost}"
					IRCD.send_to_servers(client, [], data)
				elif m == 'p':
					target.immutable = True

				target.user.modes += m
				modes += m

		elif action == '-':
			if m in target.user.modes:
				if m == 'x':
					target.setinfo(info=target.user.realhost, t="host")
					data = f":{target.id} SETHOST :{target.user.cloakhost}"
					IRCD.send_to_servers(client, [], data)
				elif m == 'p':
					target.immutable = False
				elif m == 's':
					target.user.snomask = ''
				elif m == 'o':
					if target.local:
						target.local.flood_penalty = 0
					# User de-opered. Also removing relevant oper modes.
					for opermode in [m for m in target.user.modes if IRCD.get_usermode_by_flag(m).unset_on_deoper]:
						target.user.modes = target.user.modes.replace(opermode, '')
						modes += opermode if opermode != 'o' else ''
					target.user.snomask = target.user.snomask = ''
					if target.local:
						for channel in target.channels:
							if 'O' in channel.modes:
								do_kick(target, channel, target, f"{target.name} is no longer an IRC operator")

				target.user.modes = target.user.modes.replace(m, '')
				modes += m

	if recv[0].lower() == "svs2mode" and target.local and target.user.modes != oldumodes and len(modes) > 1:
		data = f":{client.name} MODE {target.name} {modes}"
		target.send([], data)

	data = f":{client.id} {' '.join(recv)}"
	IRCD.send_to_servers(client, [], data)


def cmd_svssno(client, recv):
	if not (target := IRCD.find_user(recv[1])):
		return

	action = ''
	snomasks = ''
	for m in recv[2]:
		if m in '+-' and m != action:
			action = m
			snomasks += action
			continue
		if action == '+':
			if recv[0].lower() == 'svssno':
				target.snomasks += m
			snomasks += m

		elif action == '-':
			if recv[0].lower() == 'svssno':
				target.snomasks = target.snomasks.replace(m, '')
			snomasks += m

	cmd_mode = Command.find_command(client, "MODE")
	cmd_mode.do(client, "MODE", target.name, "+s", snomasks)

	data = ' '.join(recv)
	IRCD.send_to_servers(client, [], data)


def init(module):
	Command.add(module, cmd_svsmode, "SVSMODE", 2, Flag.CMD_SERVER)
	Command.add(module, cmd_svsmode, "SVS2MODE", 2, Flag.CMD_SERVER)
	Command.add(module, cmd_svssno, "SVSSNO", 2, Flag.CMD_SERVER)
	Command.add(module, cmd_svssno, "SVS2SNO", 2, Flag.CMD_SERVER)
