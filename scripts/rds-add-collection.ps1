$pool = 'RDS Session Collection';
$desc = 'Created by the RDS App';
$name = $env:COMPUTERNAME
$domain = "example.com"
$fqdn = "$name.$domain"

New-RDSessionCollection `
  -CollectionName $pool `
  -SessionHost "sh1.example.com" `
  -CollectionDescription $desc `
  -ConnectionBroker $fqdn
