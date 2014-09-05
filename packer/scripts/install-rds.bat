powershell -File %~dp0install-ad.ps1

schtasks /create /tn "Install RDS - RDS Features" /tr %~dp0install-rds-features.bat /sc onlogon
shutdown /r /t 5 /f /c "Install RDS - Installing AD Finished"

