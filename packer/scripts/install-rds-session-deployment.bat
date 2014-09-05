:: Deleting old scheduled task
schtasks /delete /tn "Install RDS - New Session Deployment" -f

:: Schedule next step
:: schtasks /create /tn "Install RDS Step 3" /tr %~dp0install-rds-step3.bat /sc onlogon

:: Install RDS Step 2
powershell -File %~dp0install-rds-session-deployment.ps1

:: RDS Install is doing a restart

