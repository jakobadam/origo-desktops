$password = 'V@grant' | ConvertTo-SecureString -AsPlainText -Force
$user = 'example.com\jakob'
$credential = New-Object System.Management.Automation.PSCredential($user, $password)
#Add-Computer -Credential $credential -DomainName 'example.com'