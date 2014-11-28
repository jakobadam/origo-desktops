#!/usr/bin/env python
import winrm
import os
import logging

log = logging.getLogger(__name__)

HERE = os.path.dirname(os.path.abspath(__file__))

def run_cmd(command, host, **kwargs):
    return run(command, host, interpreter='cmd', **kwargs)

def run_ps(command, host, **kwargs):
    return run(command, host, interpreter='ps', **kwargs)

def run_script(fd, host, **kwargs):
    ext = os.path.splitext(fd.name)[1]
    command = fd.read()

    if "ps" in ext:
        return run(command, host, interpreter='ps', **kwargs)

    return run(command, host, interpreter='ps', **kwargs)

def run(command, host,
    interpreter='cmd',
    auth=None,
    args=None
    ):
    """Runs a remote command.
    Returns result string

    :param command: command to execute
    :param host: host to execute on
    :param auth: (optional) Auth tuple to enable Auth.
    :param args: (optional) Tuple of command arguments.
    :param interpreter: (optional) Interpreter to use cmd or ps. Set to 'cmd' by default.

    """
    session = winrm.Session(host, auth=auth)
    if interpreter == 'cmd':
        response = session.run_cmd(command, args)
    else:
        response = session.run_ps(command, args)
    return response.std_out.rstrip('\n')

def hostname(host, name=None, **kwargs):
    """Get or set the system's host name

    :param host: host to execute command on
    :param name: (optional) set hostname to this
    """
    if not name:
        return run('hostname', host, **kwargs)
    else:
        ps = 'Rename-Computer -Restart -NewName "{}"'.format(name)
        return run_ps(ps, host, **kwargs)

def dns(host, ips=(), **kwargs):
    """Get or set DNS for the host

    :param host:
    """
    if not ips:
        script = open('{}/scripts/dns-get.ps1'.format(HERE))
        return run_script(script, host, **kwargs)
    else:
        script = open('{}/scripts/dns-set.ps1'.format(HERE))
        return run_script(script, host, args=ips, **kwargs)
    # ps = 'ls'
    # ps = '(Get-DncClientServerAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4).ServerAddresses'
    # return run_ps(ps, host, **kwargs)

def domain(host, name=None):
    """Get or set the system's domain name

    :param host: host to execute command on
    :param name: (optional) if present sets the domain to this value
    """
    if not name:
        return session.run_ps('Get-ADDomain | Select -expand DNSRoot')
    else:
        pass
        #TODO

def whereis(host, name, **kwargs):
    script = open('{}/scripts/whereis.ps1'.format(HERE))
    return run_script(script, host, args=[name], **kwargs)

if __name__ == '__main__':
    ip = '192.168.123.72'
    user = 'vagrant'
    password = 'V@grant'
    # set_session(winrm.Session(ip, auth=(user, password), transport='kerberos'))
    # print dns(ip, ips=('8.8.8.8','8.8.4.4'), auth=(user,password))
    print dns(ip, auth=(user,password))    
    # print whereis(ip, '*', auth=(user,password))    
