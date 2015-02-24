$interface = Get-DnsClientServerAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4
ForEach($ip in $interface.ServerAddresses){
    echo "$ip"
}