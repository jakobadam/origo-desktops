function usage(){
    $path = $MyInvocation.ScriptName
    echo "Usage: powershell $path DNS"
}

if($args.Count -eq 0){
    echo 'Error. Missing DNS argument'
    usage
    exit 1
}

$dns_server = $args[0]
netsh dnsclient set dnsservers name="Ethernet" source=static address="$dns_server"
