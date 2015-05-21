# Get or set the domain of the computer 
#
# If user, domain and password arguments
# are supplied the script joins the computer to the domain

$user = $args[0]
$domain = $args[1]
$password = $args[2]

if(!$domain){
    [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName
}
else{
    $password = $password | ConvertTo-SecureString -AsPlainText -Force
    $credential = New-Object System.Management.Automation.PSCredential($user, $password)
    Add-Computer -Credential $credential -DomainName $domain
}
