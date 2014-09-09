set current_task="Install RDS - Deployment"
set current_task_script="%~dp0rds-add-deployment.ps1"

schtasks /delete /tn %current_task% -f
powershell -File %current_task_script%

%~dp0install-rds-4-collection.bat



