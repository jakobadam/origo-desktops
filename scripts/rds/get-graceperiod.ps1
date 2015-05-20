# Get the number of trial days left
# Must be executed on a RDS Session Host server

$settings = Get-WmiObject -Class Win32_TerminalServiceSetting -Namespace root\CIMV2\TerminalServices
$settings.GetGracePeriodDays().DaysLeft