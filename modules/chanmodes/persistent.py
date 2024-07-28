"""
channel mode +P (persistent)
"""

from handle.core import Channelmode


def init(module):
    Cmode_P = Channelmode()
    Cmode_P.flag = 'P'
    Cmode_P.is_ok = Channelmode.allow_opers
    Cmode_P.level = 7
    Cmode_P.desc = "Channel is persistent and will not disappear when empty"
    Channelmode.add(module, Cmode_P)
