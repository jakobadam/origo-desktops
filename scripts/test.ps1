$user = 'example.com\jakob'
$password = ConvertTo-SecureString -AsPlainText -Force -String V@grant
$cred = New-Object System.Management.Automation.PSCredential($user, $password)

$session = New-PSSession rds.example.com -Credential $cred 

Invoke-Command -ScriptBlock {
    import-module RemoteDesktop
    Get-RDServer
} -Session $session
