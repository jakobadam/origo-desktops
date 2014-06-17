$fqdn = "$env:computername.$env:userdnsdomain"
New-RDSessionCollection -CollectionName Collection -SessionHost $fqdn -ConnectionBroker $fqdn