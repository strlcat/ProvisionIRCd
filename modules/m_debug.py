"""
/debug command (DANGEROUS!)
Syntax: /debug <python code>

Install this dependency manually to confirm intent: pip install -U RestrictedPython
"""
from handle.core import IRCD, Numeric, Command, Flag, Snomask
from handle.logger import logging

from io import StringIO
from contextlib import redirect_stdout
import traceback
from pprint import pprint
from RestrictedPython import compile_restricted as compile
from RestrictedPython.PrintCollector import PrintCollector
from RestrictedPython.Eval import default_guarded_getiter, default_guarded_getitem
from RestrictedPython.Guards import safe_builtins, guarded_iter_unpack_sequence, safer_getattr, full_write_guard

safe_builtins['__metaclass__'] = type
safe_builtins['_print_'] = PrintCollector
safe_builtins['_getiter_'] = default_guarded_getiter
safe_builtins['_getitem_'] = default_guarded_getitem
safe_builtins['_write_'] = full_write_guard
safe_builtins['_iter_unpack_sequence_'] = guarded_iter_unpack_sequence
safe_builtins['pprint'] = pprint
safe_builtins['vars'] = vars
safe_builtins['traceback'] = traceback

import handle.core as core; safe_builtins['core'] = core
import handle.logger as logger; safe_builtins['logger'] = logger
import handle.functions as functions; safe_builtins['functions'] = functions
import handle.client as client_; safe_builtins['client'] = client_
import handle.handleLink as handleLink; safe_builtins['handleLink'] = handleLink
import handle.log as log; safe_builtins['log'] = log
import handle.sockets as sockets; safe_builtins['sockets'] = sockets
import handle.validate_conf as validate_conf; safe_builtins['validate_conf'] = validate_conf

def exec_(src):
	src = src + "; result = printed;"
	myglobals = dict(__builtins__=safe_builtins)
	mylocals = {}
	try:
		f = StringIO()
		bc = compile(src, "<inline>", "exec")
		with redirect_stdout(f):
			exec(bc, myglobals, mylocals)
		s = mylocals['result']
		s += f.getvalue()
	except:
		s = traceback.format_exc()
	return s.rstrip()

def oprint(obj):
	pprint(vars(obj))
safe_builtins['oprint'] = oprint

def cmd_debug(client, recv):
	if not client.local or client.server:
		return
	if not client.is_superuser:
		client.sendnumeric(Numeric.ERR_NOPRIVILEGES)
		return

	dbgcmd = ' '.join(recv[1:])

	# we need to log this shit everywhere
	msg = f"*** /DEBUG invocation from {client.fullrealhost}: '{dbgcmd}'"
	logging.debug(msg)
	IRCD.log(client, "debug", "debug", "DEBUG", msg)

	output = exec_(dbgcmd)
	for line in output.split('\n'):
		client.sendnumeric(Numeric.RPL_DEBUG, line)

def init(module):
	Command.add(module, cmd_debug, "DEBUG", 1, Flag.CMD_OPER)
	Snomask.add(module, 'D', 0, "View on-server /DEBUG invocations")
