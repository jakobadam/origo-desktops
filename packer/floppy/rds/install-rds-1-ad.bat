set current_task="Install RDS - Installing AD"
set current_task_script="%~dp0install-ad.ps1"

set next_task="Install RDS - RDS Features"
set next_task_script="%~dp0install-rds-2-features.bat"

schtasks /create /tn $next_task /tr %next_task_script% /sc onlogon
powershell -File %current_task_script%

::shutdown /r /t 1 /f /c "%current_task% Finished"