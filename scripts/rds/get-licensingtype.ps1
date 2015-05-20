# Get licensingtype
# More: https://msdn.microsoft.com/en-us/library/aa383640(v=vs.85).aspx
#
# 0 Personal RD Session Host server.
# 1 Remote Desktop for Administration.
# 2 Per Device. Valid for application servers.
# 4 Per User. Valid for application servers.
# 5 Not configured.

$settings = Get-WmiObject -Class Win32_TerminalServiceSetting -Namespace root\CIMV2\TerminalServices
$settings.LicensingType
