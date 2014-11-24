#!/usr/bin/env python
import winrm
import os
import logging

log = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))

log.error('wii')
session = None

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

def set_session(s):
    global session
    session = s
    
if __name__ == '__main__':    
    ip = '192.168.123.71'
    user = 'Vagrant'
    # set_session(winrm.Session(ip, auth=(user, password), transport='kerberos'))
    set_session(winrm.Session(ip, auth=(user, password)))
    res = whereis('')
    print res.std_out
