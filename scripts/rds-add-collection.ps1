$pool = 'Session Collection';
$desc = '';
$name = $env:COMPUTERNAME
$domain = "example.com"
$fqdn = "$name.$domain"

New-RDSessionCollection `
  -CollectionName $pool `
  -SessionHost $fqdn `
  -CollectionDescription $desc `
  -ConnectionBroker $fqdn
