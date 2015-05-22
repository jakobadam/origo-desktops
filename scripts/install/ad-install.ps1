$user = $args[0]
$domain = $args[1]
$password = $args[2]

Install-WindowsFeature -Name AD-Domain-Services

# Now this module is available
Import-Module ADDSDeployment

$password = ConvertTo-SecureString -AsPlainText -Force $password

Install-ADDSForest `
    -CreateDnsDelegation:$false `
    -DatabasePath "C:\Windows\NTDS" `
    -DomainMode "Win2012R2" `
    -DomainName "$domain" `
    -DomainNetbiosName "EXAMPLE" `
    -ForestMode "Win2012R2" `
    -InstallDns:$true `
    -LogPath "C:\Windows\NTDS" `
    -NoRebootOnCompletion:$false `
    -SysvolPath "C:\Windows\SYSVOL" `
    -SafeModeAdministratorPassword $password `
    -Force:$true
