$dns_ip = $args[0]
$interfaces = Get-DnsClientServerAddress -AddressFamily IPv4 -InterfaceAlias "Ethernet*"

function usage(){
    $path = $MyInvocation.ScriptName
    echo "Usage: powershell $path DNS"
}

function get_dns(){
    ForEach($interface in $interfaces){
        ForEach($ip in $interface.ServerAddresses){
            echo "$ip"
        }
    }
}

function set_dns(){
    ForEach($interface in $interfaces){
        Set-DnsClientServerAddress -InputObject $interface -ServerAddresses $dns_ip
    }
}

if(!$dns_ip){
    get_dns
}
else{
    set_dns
}
