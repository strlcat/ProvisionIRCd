import base64
import binascii
import time
import string
import socket
from handle.logger import logging

def ip_type(ip):
    def isxdigit(s):
        return all(c in string.hexdigits for c in s)

    if isxdigit(ip.replace(':', '')):
        return socket.AF_INET6
    if ip.replace('.', '').isdigit():
        return socket.AF_INET
    return 0

def reverse_ip(ip):
    try:
        ipt = ip_type(ip)
        binip = socket.inet_pton(ipt, ip)
        revip = socket.inet_ntop(ipt, binip[::-1])
        return revip
    except Exception as ex:
        logging.exception(ex)

def valid_expire(s):
    spu = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 2592000}
    if type(s) == int:
        s = str(s)
    if s.isdigit():
        return int(s) * 60
    if s[-1] not in spu:
        return False
    try:
        return int(s[:-1]) * spu[s[-1]]
    except ValueError:
        return False

def ip_to_base64(ip):
    try:
        ipt = ip_type(ip)
        binip = socket.inet_pton(ipt, ip)
        b64ip = base64.b64encode(binip)
        b64ip = b64ip.decode()
        return b64ip
    except Exception as ex:
        logging.exception(ex)

def base64_to_ip(b64):
    try:
        binip = base64.b64decode(b64)
        n = len(binip)
        if n == 4:
            ip = socket.inet_ntop(socket.AF_INET, binip)
        elif n == 16:
            ip = socket.inet_ntop(socket.AF_INET6, binip)
        return ip
    except Exception as ex:
        logging.exception(ex)

def make_mask(data):
    nick, ident, host = '', '', ''
    nick = data.split('!')[0]
    nicklen = 32
    if nick == '' or '@' in nick or ('.' in nick and '@' not in data):
        nick = '*'
    if len(nick) > nicklen:
        nick = f'*{nick[-20:]}'
    try:
        if '@' in data:
            ident = data.split('@')[0]
            if '!' in ident:
                ident = data.split('@')[0].split('!')[1]
        else:
            ident = data.split('!')[1].split('@')[0]
    except:
        ident = '*'
    if ident == '':
        ident = '*'
    if len(ident) > 12:
        ident = f'*{ident[-12:]}'
    try:
        host = data.split('@')[1]
    except:
        if '.' in data:
            try:
                host = ''.join(data.split('@'))
            except:
                host = '*'
    if len(host) > 64:
        host = f'*{host[-64:]}'
    if host == '':
        host = '*'
    result = f'{nick}!{ident}@{host}'
    return result

def is_match(first, second):
    if not first and not second:
        return True
    if len(first) > 1 and first[0] == '*' and not second:
        return False
    if (len(first) > 1 and first[0] == '?') or (first and second and first[0] == second[0]):
        return is_match(first[1:], second[1:])
    if first and first[0] == '*':
        return is_match(first[1:], second) or is_match(first, second[1:])
    return False
