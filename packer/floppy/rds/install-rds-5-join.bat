:: Create scheduled task for reporting IP
:: Reports back every min, stops on first success
:: Copies the join.ps1 sshtask to C:

copy %~dp0join.ps1 %SystemDrive%\join.ps1
schtasks /create /tn "RDS join" /tr "powershell.exe %SystemDrive%\join.ps1" /sc minute 
