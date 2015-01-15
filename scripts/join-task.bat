copy %~dp0join.ps1 %SystemDrive%\join.ps1
schtasks /create /tn "RDS Join Task" /tr "powershell %SystemDrive%\join.ps1" /sc minute 
