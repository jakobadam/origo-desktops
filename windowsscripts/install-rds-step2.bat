schtasks /delete /tn "RDS Install Step 2" -f
powershell.exe -File \\ubuntu\source\windowsscripts\rds-install-step2.ps1
shutdown /r /t 10 /f /c "RDS Install Shutdown Step 2 Finished"