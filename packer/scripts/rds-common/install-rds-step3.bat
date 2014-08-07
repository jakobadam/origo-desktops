:: Deleting old scheduled task
schtasks /delete /tn "Install RDS Step 3" -f

:: Installing Cygwin

cmd /c %~dp0install-cygwin-sshd.bat
cmd /c %~dp0vagrant-ssh.bat

:: Schedule callback to admin server

cmd /c %~dp0ip-task.bat
