net user administrator "V@grant" /passwordreq:yes
# Must be a strong password
$password = ConvertTo-SecureString -AsPlainText -Force "V@grant"
# Must be FQDN
$domain = "example.com"
Install-ADDSForest -DomainName $domain -SafeModeAdministratorPassword $password -Force
