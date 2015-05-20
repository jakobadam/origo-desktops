# Single Server RDS deployment, i.e. the server contains all components of RDS
# Remember to run as Domain Administrator
Import-Module RemoteDesktop



# Can't be run from the server itself. Because it can't restart itself?!?
# $fqdn = [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName
$fqdn = 'rds.example.com'

New-RDSessionDeployment -ConnectionBroker $fqdn `
    -WebAccessServer $fqdn `
    -SessionHost $fqdn

New-RDSessionCollection -CollectionName 'App Collection' `
   -SessionHost $fqdn `
   -CollectionDescription 'Desc' `
   -ConnectionBroker $fqdn 