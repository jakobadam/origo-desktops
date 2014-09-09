set current_task="Install RDS - RDS Features"
set current_task_script="%~dp0install-rds-2-features.ps1"

set next_task="Install RDS - Deployment"
set next_task_script="%~dp0install-rds-3-deployment.bat"

schtasks /delete /tn %current_task% -f
powershell -File %current_task_script%

schtasks /create /tn %next_task% /tr %next_task_script% /sc onlogon
shutdown /r /t 1 /f /c "%current_task% Finished"
