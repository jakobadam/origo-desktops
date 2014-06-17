#echo $Host
$fqdn = "$env:computername.$env:userdnsdomain"
New-RDSessionDeployment -ConnectionBroker $fqdn -WebAccessServer $fqdn -SessionHost $fqdn