$interface = Get-DnsClientServerAddress -InterfaceAlias "Ethernet" -AddressFamily IPv4
Set-DnsClientServerAddress -InputObject $interface -ServerAddresses $args
