$user = $args[0]
$password = $args[1]
$domain = $args[2]

if(!$domain){
    [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName
}
else{
    $password = $password | ConvertTo-SecureString -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($user, $password)
    Add-Computer -Credential $credential -DomainName 'example.com'
}
