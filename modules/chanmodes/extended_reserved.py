"""
channel mode +X (eXtended modes)
Currently a reserved list mode, not available to anyone.
Format: +X <extspec> <extparam>
"""

from handle.core import Channelmode

def init(module):
	Channelmode.add_generic('X')
