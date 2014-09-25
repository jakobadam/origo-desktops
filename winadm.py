#!/usr/bin/env python
import winrm
import os

import parser

HERE = os.path.dirname(__file__)

ip = '192.168.123.151'
user = 'vagrant'
password = 'V@grant'

session = winrm.Session(ip, auth=(user, password))

def insert_ps_args(script, args=()):
    for i,arg in enumerate(args):
        old = "$args[{}]".format(i)
        new = '"{}"'.format(arg)
        script = script.replace(old, new)
    return script

def run_script(fd, args=()):
    ext = os.path.splitext(fd.name)[1]
    content = fd.read()

    if "ps" in ext:
        if args:
            content = insert_ps_args(content, args)
        return session.run_ps(content)
    else:
        return session.run_cmd(content, *args)

def hostname(name=None, **kwargs):
    """Get or set the system's host name
    """
    if not name:
        return session.run_cmd('hostname')
    else:
        return session.run_ps('Rename-Computer -Restart -NewName "%s"' % name)

def domain(name=None):
    """Get or set the system's domain name
    """
    if not name:
        return session.run_ps('Get-ADDomain | Select -expand DNSRoot')
    else:
        pass
        #TODO

def whereis(name):
    script = open('{}/scripts/whereis.ps1'.format(HERE))
    return run_script(script, args=[name])

# def _enable_log():
#     import logging
#     log = logging.getLogger('winexe')
#     log.setLevel(logging.DEBUG)
#     handler = logging.StreamHandler()
#     log.addHandler(handler)

if __name__ == '__main__':    
    #print whereis('word', **kwargs)
    res = whereis('firefox')
    print res.std_err
    print res.std_out
