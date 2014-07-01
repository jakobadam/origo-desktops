$password = ConvertTo-SecureString -AsPlainText -Force "V@grant"
$domain = "example.com"

# RDS Deployment
$fqdn = "$env:computername.$env:userdnsdomain"
New-RDSessionDeployment -ConnectionBroker $fqdn -WebAccessServer $fqdn -SessionHost $fqdn