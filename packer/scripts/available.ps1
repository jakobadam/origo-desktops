#$pool = 'Session Collection';

#Get-RDAvailableApp -CollectionName $pool

#Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | select installLocation
    
# List installed programs - I think installed through msiexec
# The program location is not in there:(
Get-WmiObject -class win32_product | select *

#wmic product

