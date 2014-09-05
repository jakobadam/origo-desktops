Install-WindowsFeature -Name AD-Domain-Services

# Now this module is available
Import-Module ADDSDeployment

$domain = "example.com"
$password = ConvertTo-SecureString -AsPlainText -Force "V@grant"

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
