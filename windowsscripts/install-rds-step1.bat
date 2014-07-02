powershell.exe -File \\ubuntu\source\windowsscripts\rds-install-step1.ps1
schtasks /create /tn "RDS Install Step 2" /tr \\ubuntu\source\windowsscripts\rds-install-step2.bat /sc onlogon
shutdown /r /t 5 /f /c "RDS Install Shutdown Step 1 Finished"


