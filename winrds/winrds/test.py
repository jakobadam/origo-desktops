import subprocess
import os

def test():
    #f = open(r'C:\winrds\winrds\views.py')
    #f = open(r'C:\Windows\System32\WindowsPowerShell\v1.0\Modules\RemoteDesktop\Certificate.psm1', 'r')
    #f = open(r'C:\Windows\System32\indowsPowerShell', 'r')
    #print f.read()
    
    cmd = [
        'powershell',
        './scripts/rds-get-apps2.ps1'
    ]
    #output = os.getcwd()
    output = subprocess.check_output(cmd, shell=True)
    print output
    ##output = subprocess.check_output('echo %PATH%', shell=True)
    

if __name__ == '__main__':
    test()
