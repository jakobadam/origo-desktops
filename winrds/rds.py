from __future__ import print_function

import subprocess
import os
import sys

HERE = os.path.abspath(os.path.dirname(__name__))

print('HERE: {}'.format(HERE))

def run(path, *args):
    cmd = [
        r'%SystemRoot%\SysWoW64\WindowsPowerShell\v1.0\powershell.exe',
        path
    ]
    
    # surround arg with " e.g. my arg becomes -> "my arg"
    for a in args:
        cmd.append('"{}"'.format(a))    
    
    try:
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT, cwd=os.getcwd())
        output = output.strip('\r\n')
        return output
    except subprocess.CalledProcessError, e:
        err = e.output.strip('\r\n')
        print(err)
        sys.exit(1)

def collections():
    _list = run('./scripts/collections.ps1').split('\r\n')
    return _list

def applications(collection):
    _list = run('./scripts/applications.ps1', collection).split('\r\n')
    return _list

def info():
    return run('./scripts/info.ps1')

if __name__ == '__main__':
    print(info())
