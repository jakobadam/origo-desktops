:: Delete old sch. task
schtasks /delete /tn "Install RDS - RDS Features" -f

powershell -File %~dp0install-rds-features.ps1

:: Scheduling Install RDS Step 2
schtasks /create /tn "Install RDS - New Session Deployment" /tr %~dp0install-rds-session-deployment.bat /sc onlogon
shutdown /r /t 5 /f /c "Install RDS - Installing RDS Features Finished"
