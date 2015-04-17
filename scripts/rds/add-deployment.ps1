Import-Module RemoteDesktop

#$fqdn = [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName
$fqdn = 'rds-new.example.com'

New-RDSessionDeployment -ConnectionBroker $fqdn `
    -WebAccessServer $fqdn `
    -SessionHost $fqdn

New-RDSessionCollection -CollectionName 'My collection' `
   -SessionHost $fqdn `
   -CollectionDescription 'Desc' `
   -ConnectionBroker $fqdn 