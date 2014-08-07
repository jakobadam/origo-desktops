:: Create scheduled task for reporting IP
:: Reports back every min, stops on first success
schtasks /create /tn "rds-report-ip" /tr "powershell.exe %~dp0join.ps1" /sc minute 