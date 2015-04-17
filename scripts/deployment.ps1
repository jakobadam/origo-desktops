Import-Module RemoteDesktop

$fqdn = [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName

New-RDSessionDeployment `
  -ConnectionBroker $fqdn `
  -WebAccessServer $fqdn `
  -SessionHost $fqdn

# New-RDSessionDeployment : Validation failed for the "RD Session Host" parameter.
# RDS.EXAMPLE.COM      You cannot restart the local server.
