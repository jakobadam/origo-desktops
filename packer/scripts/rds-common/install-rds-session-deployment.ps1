$name = $env:COMPUTERNAME
$domain = "example.com"
$fqdn = "$name.$domain"

New-RDSessionDeployment -ConnectionBroker $fqdn -WebAccessServer $fqdn -SessionHost $fqdn
